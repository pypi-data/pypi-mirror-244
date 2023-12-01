n__author__ = "Simon Nilsson"

import pandas as pd
import numpy as np
import os
import cv2
from numba import jit, prange
import platform
import multiprocessing
import functools
from typing import List

from simba.utils.enums import Formats, TagNames
from simba.mixins.config_reader import ConfigReader
from simba.mixins.plotting_mixin import PlottingMixin
from simba.utils.errors import NoSpecifiedOutputError
from simba.utils.printing import stdout_success, SimbaTimer, log_event
from simba.utils.read_write import get_fn_ext, remove_a_folder, concatenate_videos_in_folder, read_df

def _heatmap_location(data: np.array,
                     video_setting: bool,
                     frame_setting: bool,
                     video_temp_dir: str,
                     video_name: str,
                     frame_dir: str,
                     fps: int,
                     style_attr: dict,
                     max_scale: float,
                     aspect_ratio: float,
                     size: tuple,
                     make_location_heatmap_plot: PlottingMixin.make_location_heatmap_plot):

    group = int(data[0][0][1])
    if video_setting:
        fourcc = cv2.VideoWriter_fourcc(*Formats.MP4_CODEC.value)
        video_save_path = os.path.join(video_temp_dir, '{}.mp4'.format(str(group)))
        video_writer = cv2.VideoWriter(video_save_path, fourcc, fps, size)


    for i in range(data.shape[0]):
        frame_id = int(data[i, 0, 0])
        frm_data = data[i, :, 2:]

        img = make_location_heatmap_plot(frm_data=frm_data,
                                         max_scale= float(max_scale),
                                         palette= style_attr['palette'],
                                         aspect_ratio= aspect_ratio,
                                         shading=style_attr['shading'],
                                         img_size=size,
                                         file_name=None,
                                         final_img=False)

        print('Heatmap frame created: {}, Video: {}, Processing core: {}'.format(str(frame_id+1), video_name, str(group+1)))

        if video_setting:
            video_writer.write(img)

        if frame_setting:
            file_path = os.path.join(frame_dir, '{}.png'.format(frame_id))
            cv2.imwrite(file_path, img)

    if video_setting:
        video_writer.release()

    return group

class HeatMapperLocationMultiprocess(ConfigReader, PlottingMixin):

    """
    Create heatmaps representing the locations of animal body-part. Uses multiprocessing.

    :param str config_path: path to SimBA project config file in Configparser format
    :param str bodypart: The name of the body-part used to infer the location of the classified behavior
    :param int bin_size: The rectangular size of each heatmap location in millimeters. For example, `50` will divide the video frames
        into 5 centimeter rectangular spatial bins.
    :param str palette:  Heatmap pallette. Eg. 'jet', 'magma', 'inferno','plasma', 'viridis', 'gnuplot2'
    :param int or 'auto' max_scale: The max value in the heatmap in seconds. E.g., with a value of `10`, if the classified behavior has occured
        >= 10 within a rectangular bins, it will be filled with the same color.
    :param bool final_img_setting: If True, create a single image representing the last frame of the input video
    :param bool video_setting: If True, then create a video of heatmaps.
    :param bool frame_setting: If True, then create individual heatmap frames.
    :param int core_cnt: Number of cores to use.

    .. note::
       `GitHub visualizations tutorial <https://github.com/sgoldenlab/simba/blob/master/docs/tutorial.md#step-11-visualizations>`__.

    Examples
    -----
    >>> heat_mapper_clf = HeatMapperLocationMultiprocess(config_path='MyConfigPath', final_img_setting=False, video_setting=True, frame_setting=False, bin_size=50, palette='jet', bodypart='Nose_1', clf_name='Attack', max_scale=20).run()
    """

    def __init__(self,
                 config_path: str,
                 final_img_setting: bool,
                 video_setting: bool,
                 frame_setting: bool,
                 bodypart: str,
                 files_found: List[str],
                 style_attr: dict,
                 core_cnt: int
                 ):

        ConfigReader.__init__(self, config_path=config_path)
        PlottingMixin.__init__(self)
        log_event(logger_name=str(__class__.__name__), log_type=TagNames.CLASS_INIT.value, msg=self.create_log_msg_from_init_args(locals=locals()))
        if platform.system() == "Darwin":
            multiprocessing.set_start_method('spawn', force=True)

        if (not frame_setting) and (not video_setting) and (not final_img_setting):
            raise NoSpecifiedOutputError(msg='Please choose to select either heatmap videos, frames, and/or final image.', source=self.__class__.__name__)
        self.frame_setting, self.video_setting = frame_setting, video_setting
        self.final_img_setting, self.bp = final_img_setting, bodypart
        self.style_attr, self.files_found = style_attr, files_found
        self.bin_size, self.max_scale, self.palette, self.shading, self.core_cnt = style_attr['bin_size'], style_attr['max_scale'], style_attr['palette'], style_attr['shading'], core_cnt
        if not os.path.exists(self.heatmap_location_dir): os.makedirs(self.heatmap_location_dir)
        self.bp_lst = [self.bp + '_x', self.bp + '_y']
        print('Processing {} video(s)...'.format(str(len(self.files_found))))

    @staticmethod
    @jit(nopython=True)
    def __calculate_cum_array(clf_array: np.array,
                              fps: int):
        cum_sum_arr = np.full(clf_array.shape, np.nan)
        for frm_idx in prange(clf_array.shape[0]):
            frame_cum_sum = np.full((clf_array.shape[1], clf_array.shape[2]), 0.0)
            sliced_arr = clf_array[0:frm_idx]
            for i in range(sliced_arr.shape[0]):
                for j in range(sliced_arr.shape[1]):
                    for k in range(sliced_arr.shape[2]):
                        frame_cum_sum[j][k] += sliced_arr[i][j][k]
            cum_sum_arr[frm_idx] = frame_cum_sum


        return cum_sum_arr / fps

    @staticmethod
    @jit(nopython=True)
    def __insert_group_idx_column(data: np.array,
                                  group: int,
                                  last_frm_idx: int):


        results = np.full((data.shape[0], data.shape[1], data.shape[2]+2), np.nan)
        group_col = np.full((data.shape[1], 1), group)
        for frm_idx in prange(data.shape[0]):
            h_stack = np.hstack((group_col, data[frm_idx]))
            frm_col = np.full((h_stack.shape[0], 1), frm_idx+last_frm_idx)
            results[frm_idx] = np.hstack((frm_col, h_stack))

        return results

    def __calculate_bin_attr(self,
                             data_df: pd.DataFrame,
                             bp_lst: list,
                             px_per_mm: int,
                             img_width: int,
                             img_height: int,
                             bin_size: int,
                             fps: int):

        bin_size_px = int(float(px_per_mm) * float(bin_size))
        horizontal_bin_cnt = int(img_width / bin_size_px)
        vertical_bin_cnt = int(img_height / bin_size_px)
        aspect_ratio = round((vertical_bin_cnt / horizontal_bin_cnt), 3)

        bp_data = data_df[bp_lst].to_numpy().astype(int)

        bin_dict = {}
        x_location, y_location = 0, 0
        for hbin in range(horizontal_bin_cnt):
            bin_dict[hbin] = {}
            for vbin in range(vertical_bin_cnt):
                bin_dict[hbin][vbin] = {'top_left_x': x_location,
                                        'top_left_y': y_location,
                                        'bottom_right_x': x_location + bin_size_px,
                                        'bottom_right_y': y_location + bin_size_px}
                y_location += bin_size_px
            y_location = 0
            x_location += bin_size_px

        location_array = np.zeros((bp_data.shape[0], vertical_bin_cnt, horizontal_bin_cnt))

        for frm_cnt, frame in enumerate(bp_data):
            for h_bin_name, v_dict in bin_dict.items():
                for v_bin_name, c in v_dict.items():
                    if (frame[0] <= c['bottom_right_x'] and frame[0] >= c['top_left_x']):
                        if (frame[1] <= c['bottom_right_y'] and frame[0] >= c['top_left_y']):
                            location_array[frm_cnt][v_bin_name][h_bin_name] = 1

        location_array = self.__calculate_cum_array(clf_array=location_array, fps=fps)

        return location_array, aspect_ratio

    def __calculate_max_scale(self,
                              clf_array: np.array):
        return np.round(np.max(np.max(clf_array[-1], axis=0)), 3)

    def run(self):
        '''
        Creates heatmap charts. Results are stored in the `project_folder/frames/heatmaps_classifier_locations`
        directory of SimBA project.

        Returns
        ----------
        None
        '''

        for file_cnt, file_path in enumerate(self.files_found):
            video_timer = SimbaTimer(start=True)
            _, self.video_name, _ = get_fn_ext(file_path)
            self.video_info, self.px_per_mm, self.fps = self.read_video_info(video_name=self.video_name)
            self.width, self.height = int(self.video_info['Resolution_width'].values[0]), int(self.video_info['Resolution_height'].values[0])
            self.save_frame_folder_dir = os.path.join(self.heatmap_location_dir, self.video_name)
            self.video_folder = os.path.join(self.heatmap_location_dir, self.video_name)
            self.temp_folder = os.path.join(self.heatmap_location_dir, self.video_name, 'temp')
            if self.frame_setting:
                if os.path.exists(self.save_frame_folder_dir):
                    remove_a_folder(folder_dir=self.save_frame_folder_dir)
                if not os.path.exists(self.save_frame_folder_dir): os.makedirs(self.save_frame_folder_dir)
            if self.video_setting:
                if os.path.exists(self.temp_folder):
                    remove_a_folder(folder_dir=self.temp_folder)
                    remove_a_folder(folder_dir=self.video_folder)
                os.makedirs(self.temp_folder)
                self.save_video_path = os.path.join(self.heatmap_location_dir, f'{self.video_name}.mp4')

            self.data_df = read_df(file_path=file_path, file_type=self.file_type)
            location_array, aspect_ratio = self.__calculate_bin_attr(data_df=self.data_df,
                                                                bp_lst=self.bp_lst,
                                                                px_per_mm=self.px_per_mm,
                                                                img_width=self.width,
                                                                img_height=self.height,
                                                                bin_size=self.bin_size,
                                                                fps=self.fps)


            if self.max_scale == 'auto':
                self.max_scale = self.__calculate_max_scale(clf_array=location_array)
            else:
                self.max_scale = self.style_attr['max_scale']


            if self.final_img_setting:
                self.make_location_heatmap_plot(frm_data=location_array[-1, :, :],
                                                max_scale=self.max_scale,
                                                palette=self.palette,
                                                aspect_ratio=aspect_ratio,
                                                file_name=os.path.join(self.heatmap_location_dir, self.video_name + '_final_frm.png'),
                                                shading=self.shading,
                                                img_size=(self.width, self.height),
                                                final_img=True)

            if self.video_setting or self.frame_setting:
                frame_arrays = np.array_split(location_array, self.core_cnt)
                last_frm_idx = 0
                for frm_group in range(len(frame_arrays)):
                    split_arr = frame_arrays[frm_group]
                    frame_arrays[frm_group] = self.__insert_group_idx_column(data=split_arr, group=frm_group, last_frm_idx=last_frm_idx)
                    last_frm_idx = np.max(frame_arrays[frm_group].reshape((frame_arrays[frm_group].shape[0], -1)))
                frm_per_core = frame_arrays[0].shape[0]
                with multiprocessing.Pool(self.core_cnt, maxtasksperchild=self.maxtasksperchild) as pool:
                    constants = functools.partial(_heatmap_location,
                                                  video_setting=self.video_setting,
                                                  frame_setting=self.frame_setting,
                                                  style_attr=self.style_attr,
                                                  fps=self.fps,
                                                  video_temp_dir=self.temp_folder,
                                                  frame_dir=self.save_frame_folder_dir,
                                                  max_scale=self.max_scale,
                                                  aspect_ratio=aspect_ratio,
                                                  size=(self.width, self.height),
                                                  video_name=self.video_name,
                                                  make_location_heatmap_plot=self.make_location_heatmap_plot)

                    for cnt, result in enumerate(pool.imap(constants, frame_arrays, chunksize=self.multiprocess_chunksize)):
                        print('Image {}/{}, Video {}/{}...'.format(str(int(frm_per_core * (result + 1))),
                                                                   str(len(self.data_df)), str(file_cnt + 1),
                                                                   str(len(self.files_found))))
                    pool.terminate()
                    pool.join()

                if self.video_setting:
                    print('Joining {} multiprocessed heatmap location video...'.format(self.video_name))
                    concatenate_videos_in_folder(in_folder=self.temp_folder, save_path=self.save_video_path)

                video_timer.stop_timer()
                print('Heatmap video {} complete (elapsed time: {}s) ...'.format(self.video_name, video_timer.elapsed_time_str))

            self.timer.stop_timer()
            stdout_success(msg=f'Heatmap location videos visualizations for {len(self.files_found)} videos created in project_folder/frames/output/heatmaps_locations directory', elapsed_time=self.timer.elapsed_time_str, source=self.__class__.__name__)

# test = HeatMapperLocationMultiprocess(config_path='/Users/simon/Desktop/envs/troubleshooting/locomotion/project_folder/project_config.ini',
#                                       style_attr = {'palette': 'jet', 'shading': 'gouraud', 'bin_size': 50, 'max_scale': 'auto'},
#                                       final_img_setting=False,
#                                       video_setting=True,
#                                       frame_setting=False,
#                                       bodypart='Nose',
#                                       core_cnt=5,
#                                       files_found=['/Users/simon/Desktop/envs/troubleshooting/locomotion/project_folder/csv/outlier_corrected_movement_location/PD1406_2022-05-24_RVDG_GCaMP8s-Gi_Video_Day_22_Baseline.csv'])
# test.create_heatmaps()


# test = HeatMapperLocationMultiprocess(config_path='/Users/simon/Desktop/envs/troubleshooting/two_black_animals_14bp/project_folder/project_config.ini',
#                                       style_attr = {'palette': 'jet', 'shading': 'gouraud', 'bin_size': 50, 'max_scale': 'auto'},
#                                       final_img_setting=True,
#                                       video_setting=True,
#                                       frame_setting=False,
#                                       bodypart='Nose_1', core_cnt=5,
#                                       files_found=['/Users/simon/Desktop/envs/troubleshooting/two_black_animals_14bp/project_folder/csv/machine_results/Together_1.csv'])
# test.create_heatmaps()
