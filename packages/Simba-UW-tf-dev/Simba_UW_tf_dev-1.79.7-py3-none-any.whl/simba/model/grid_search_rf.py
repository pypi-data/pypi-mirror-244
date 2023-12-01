__author__ = "Simon Nilsson"

import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pandas as pd

from simba.utils.checks import (check_int,
                                check_str,
                                check_float,
                                check_if_filepath_list_is_empty,
                                check_if_valid_input)
from simba.utils.read_write import (read_config_entry,
                                    read_meta_file,
                                    read_simba_meta_files,
                                    get_fn_ext,
                                    str_2_bool,
                                    write_df)
from simba.ui.tkinter_functions import TwoOptionQuestionPopUp
from simba.utils.printing import stdout_success, log_event
from simba.utils.errors import InvalidInputError, NoDataError
from simba.utils.enums import (Options,
                               ConfigKey,
                               Dtypes,
                               Methods,
                               MetaKeys,
                               TagNames,
                               Formats)
from simba.mixins.config_reader import ConfigReader
from simba.mixins.train_model_mixin import TrainModelMixin


class GridSearchRandomForestClassifier(ConfigReader, TrainModelMixin):
    """
    Grid-searching random forest models from hyperparameter setting and sampling methods
    stored within the `project_folder/configs` directory of a SimBA project.

    .. note::
       Searches you SimBA project `project_folder/configs` directory for files and builds
       one model per config file. `Tutorial <https://github.com/sgoldenlab/simba/blob/master/docs/Scenario1.md#step-7-train-machine-model>`__.

    :param str config_path: path to SimBA project config file in Configparser format

    Example
    ----------
    >>> _ = GridSearchRandomForestClassifier(config_path='MyConfigPath').run()
    """

    def __init__(self,
                 config_path: str):

        ConfigReader.__init__(self, config_path=config_path)
        log_event(logger_name=str(self.__class__.__name__), log_type=TagNames.CLASS_INIT.value, msg=self.create_log_msg_from_init_args(locals=locals()))
        TrainModelMixin.__init__(self)
        self.model_dir_out = os.path.join(read_config_entry(self.config, ConfigKey.SML_SETTINGS.value, ConfigKey.MODEL_DIR.value, data_type=Dtypes.STR.value), 'validations')
        if not os.path.exists(self.model_dir_out): os.makedirs(self.model_dir_out)
        check_if_filepath_list_is_empty(filepaths=self.target_file_paths,
                                        error_msg='Zero annotation files found in project_folder/csv/targets_inserted, cannot create models.')
        if not os.path.exists(self.configs_meta_dir): os.makedirs(self.configs_meta_dir)
        self.meta_file_lst = sorted(read_simba_meta_files(self.configs_meta_dir))
        print('Reading in {} annotated files...'.format(str(len(self.target_file_paths))))
        self.data_df, self.frm_idx = self.read_all_files_in_folder_mp_futures(self.target_file_paths, self.file_type)
        self.frm_idx = pd.DataFrame({'VIDEO': list(self.data_df.index), 'FRAME_IDX': self.frm_idx})
        self.data_df = self.check_raw_dataset_integrity(self.data_df, logs_path=self.logs_path)
        self.data_df = self.drop_bp_cords(df=self.data_df)

    def perform_sampling(self, meta_dict: dict):
        if meta_dict[MetaKeys.TRAIN_TEST_SPLIT_TYPE.value] == Methods.SPLIT_TYPE_FRAMES.value:
            self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(self.x_df, self.y_df, test_size=meta_dict['train_test_size'])
        elif meta_dict[MetaKeys.TRAIN_TEST_SPLIT_TYPE.value] == Methods.SPLIT_TYPE_BOUTS.value:
            self.x_train, self.x_test, self.y_train, self.y_test = self.bout_train_test_splitter(x_df=self.x_df, y_df=self.y_df, test_size=meta_dict['train_test_size'])
        else:
            raise InvalidInputError(msg=f'{meta_dict[MetaKeys.TRAIN_TEST_SPLIT_TYPE.value]} is not recognized as a valid SPLIT TYPE (OPTIONS: FRAMES, BOUTS).', source=self.__class__.__name__)
        if meta_dict[ConfigKey.UNDERSAMPLE_SETTING.value].lower() == Methods.RANDOM_UNDERSAMPLE.value:
            self.x_train, self.y_train = self.random_undersampler(self.x_train, self.y_train, meta_dict[ConfigKey.UNDERSAMPLE_RATIO.value])
        if meta_dict[ConfigKey.OVERSAMPLE_SETTING.value].lower() == Methods.SMOTEENN.value:
            self.x_train, self.y_train = self.smoteen_oversampler(self.x_train, self.y_train, meta_dict[ConfigKey.OVERSAMPLE_RATIO.value])
        elif meta_dict[ConfigKey.OVERSAMPLE_SETTING.value].lower() == Methods.SMOTE.value:
            self.x_train, self.y_train = self.smote_oversampler(self.x_train, self.y_train, meta_dict[ConfigKey.OVERSAMPLE_RATIO.value])

        print(meta_dict[MetaKeys.SAVE_TRAIN_TEST_FRM_IDX.value])
        if meta_dict[MetaKeys.SAVE_TRAIN_TEST_FRM_IDX.value]:
            train_data = self.frm_idx[self.frm_idx.index.isin(self.x_train.index)].set_index('VIDEO')
            test_data = self.frm_idx[self.frm_idx.index.isin(self.x_test.index)].set_index('VIDEO')
            write_df(df=train_data, file_type=Formats.CSV.value, save_path=os.path.join(self.model_dir_out, f'train_idx_model_{self.config_cnt}.csv'))
            write_df(df=test_data, file_type=Formats.CSV.value, save_path=os.path.join(self.model_dir_out, f'test_idx_{self.config_cnt}.csv'))
            print(f'Frame index for train and test set in model {self.config_cnt} saved in {self.model_dir_out} directory...')

    def run(self):
        self.meta_dicts = self.check_validity_of_meta_files(data_df=self.data_df, meta_file_paths=self.meta_file_lst)
        if len(self.meta_dicts.keys()) == 0:
            raise NoDataError(msg='No valid hyper-parameter config files', source=self.__class__.__name__)
        for config_cnt, meta_dict in self.meta_dicts.items():
            self.config_cnt = config_cnt
            self.clf_name = meta_dict[MetaKeys.CLF_NAME.value]
            print(f'Training model {config_cnt+1}/{len(self.meta_dicts.keys())} ({meta_dict[MetaKeys.CLF_NAME.value]})...')
            self.class_names = [f'Not_{meta_dict[MetaKeys.CLF_NAME.value]}', meta_dict[MetaKeys.CLF_NAME.value]]
            annotation_cols_to_remove = self.read_in_all_model_names_to_remove(self.config, self.clf_cnt, meta_dict[MetaKeys.CLF_NAME.value])
            self.x_y_df = self.delete_other_annotation_columns(self.data_df, annotation_cols_to_remove)
            self.x_df, self.y_df = self.split_df_to_x_y(self.x_y_df, meta_dict[MetaKeys.CLF_NAME.value])
            self.feature_names = self.x_df.columns
            self.check_sampled_dataset_integrity(x_df=self.x_df, y_df=self.y_df)
            self.perform_sampling(meta_dict=meta_dict)
            print(f'MODEL {config_cnt+1} settings')
            self.print_machine_model_information(meta_dict)
            print('# {} features.'.format(len(self.feature_names)))
            self.rf_clf = RandomForestClassifier(n_estimators=meta_dict[MetaKeys.RF_ESTIMATORS.value],
                                                 max_features=meta_dict[MetaKeys.RF_MAX_FEATURES.value],
                                                 n_jobs=-1,
                                                 criterion=meta_dict[MetaKeys.CRITERION.value],
                                                 min_samples_leaf=meta_dict[MetaKeys.MIN_LEAF.value],
                                                 bootstrap=True,
                                                 verbose=1,
                                                 class_weight=meta_dict[ConfigKey.CLASS_WEIGHTS.value])

            print(f'Fitting {self.clf_name} model...')
            self.rf_clf = self.clf_fit(clf=self.rf_clf, x_df=self.x_train, y_df=self.y_train)
            if meta_dict[MetaKeys.PERMUTATION_IMPORTANCE.value] in Options.PERFORM_FLAGS.value:
                self.calc_permutation_importance(self.x_test, self.y_test, self.rf_clf, self.feature_names, self.clf_name, self.model_dir_out, save_file_no=config_cnt)
            if meta_dict[MetaKeys.LEARNING_CURVE.value] in Options.PERFORM_FLAGS.value:
                self.calc_learning_curve(self.x_y_df, self.clf_name, meta_dict[MetaKeys.LEARNING_CURVE_K_SPLITS.value], meta_dict[MetaKeys.LEARNING_CURVE_DATA_SPLITS.value], meta_dict[MetaKeys.TT_SIZE.value], self.rf_clf, self.model_dir_out, save_file_no=config_cnt)
            if meta_dict[MetaKeys.PRECISION_RECALL.value] in Options.PERFORM_FLAGS.value:
                self.calc_pr_curve(self.rf_clf, self.x_test, self.y_test, self.clf_name, self.model_dir_out, save_file_no=config_cnt)
            if meta_dict[MetaKeys.EX_DECISION_TREE.value] in Options.PERFORM_FLAGS.value:
                self.create_example_dt(self.rf_clf, self.clf_name, self.feature_names, self.class_names, self.model_dir_out, save_file_no=config_cnt)
            if meta_dict[MetaKeys.CLF_REPORT.value] in Options.PERFORM_FLAGS.value:
                self.create_clf_report(self.rf_clf, self.x_test, self.y_test, self.class_names, self.model_dir_out, save_file_no=config_cnt)
            if meta_dict[MetaKeys.IMPORTANCE_LOG.value] in Options.PERFORM_FLAGS.value:
                self.create_x_importance_log(self.rf_clf, self.feature_names, self.clf_name, self.model_dir_out, save_file_no=config_cnt)
            if meta_dict[MetaKeys.IMPORTANCE_BAR_CHART.value] in Options.PERFORM_FLAGS.value:
                self.create_x_importance_bar_chart(self.rf_clf, self.feature_names, self.clf_name, self.model_dir_out, meta_dict[MetaKeys.N_FEATURE_IMPORTANCE_BARS.value], save_file_no=config_cnt)
            if MetaKeys.SHAP_SCORES.value in meta_dict.keys():
                save_n = meta_dict[MetaKeys.SHAP_PRESENT.value] + meta_dict[MetaKeys.SHAP_ABSENT.value]
                shap_multiprocess = False
                if MetaKeys.SHAP_SAVE_ITERATION.value in meta_dict.keys():
                    try:
                        save_n = int(meta_dict[MetaKeys.SHAP_SAVE_ITERATION.value])
                    except ValueError:
                        save_n = meta_dict[MetaKeys.SHAP_PRESENT.value] + meta_dict[MetaKeys.SHAP_ABSENT.value]
                if ConfigKey.SHAP_MULTIPROCESS.value in meta_dict.keys():
                    shap_multiprocess = meta_dict[ConfigKey.SHAP_MULTIPROCESS.value]

                if meta_dict[MetaKeys.SHAP_SCORES.value] in Options.PERFORM_FLAGS.value:
                    if not shap_multiprocess in Options.PERFORM_FLAGS.value:
                        self.create_shap_log(ini_file_path=self.config_path,
                                             rf_clf=self.rf_clf,
                                             x_df=self.x_train,
                                             y_df=self.y_train,
                                             x_names=self.feature_names,
                                             clf_name=self.clf_name,
                                             cnt_present=meta_dict[MetaKeys.SHAP_PRESENT.value],
                                             cnt_absent=meta_dict[MetaKeys.SHAP_ABSENT.value],
                                             save_path=self.model_dir_out,
                                             save_it=save_n,
                                             save_file_no=config_cnt)
                    else:
                        self.create_shap_log_mp(ini_file_path=self.config_path,
                                                rf_clf=self.rf_clf,
                                                x_df=self.x_train,
                                                y_df=self.y_train,
                                                x_names=self.feature_names,
                                                clf_name=self.clf_name,
                                                cnt_present=meta_dict[MetaKeys.SHAP_PRESENT.value],
                                                cnt_absent=meta_dict[MetaKeys.SHAP_ABSENT.value],
                                                save_path=self.model_dir_out,
                                                save_file_no=config_cnt)

            if MetaKeys.PARTIAL_DEPENDENCY.value in meta_dict.keys():
                if meta_dict[MetaKeys.PARTIAL_DEPENDENCY.value] in Options.PERFORM_FLAGS.value:
                    self.partial_dependence_calculator(clf=self.rf_clf, x_df=self.x_train, clf_name=self.clf_name, save_dir=self.model_dir_out)
            self.create_meta_data_csv_training_multiple_models(meta_dict, self.clf_name, self.model_dir_out, save_file_no=config_cnt)
            self.save_rf_model(self.rf_clf, self.clf_name, self.model_dir_out, save_file_no=config_cnt)
            print('Classifier {} saved in models/validations/model_files directory ...'.format(str(self.clf_name + '_' + str(config_cnt))))
        stdout_success(msg='All models and evaluations complete. The models/evaluation files are in models/validations folders', source=self.__class__.__name__)

# test = GridSearchRandomForestClassifier(config_path='/Users/simon/Desktop/envs/troubleshooting/sophie/project_folder/project_config.ini')
# test.run()

# test = TrainMultipleModelsFromMeta(config_path='/Users/simon/Desktop/envs/troubleshooting/locomotion/project_folder/project_config.ini')
# test.run()

# test = GridSearchRandomForestClassifier(config_path='/Users/simon/Desktop/envs/troubleshooting/two_black_animals_14bp/project_folder/project_config.ini')
# test.run()


# test = TrainMultipleModelsFromMeta(config_path='/Users/simon/Desktop/envs/troubleshooting/two_black_animals_14bp/project_folder/project_config.ini')
# test.run()

# file_paths = glob.glob('/Users/simon/Desktop/envs/troubleshooting/two_black_animals_14bp/project_folder/csv/targets_inserted' + '/*.csv')
# df = read_all_files_in_folder_mp(file_paths=file_paths, file_type='csv')
# check_dataset_integrity(df=df)

#
# test = GridSearchRandomForestClassifier(config_path='/Users/simon/Desktop/envs/troubleshooting/naresh/project_folder/project_config.ini')
# test.run()




