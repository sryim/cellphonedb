import os

import pandas as pd

from cellphonedb.src.app.flask.flask_app import create_app
from cellphonedb.src.app.cellphonedb_app import output_test_dir, data_test_dir, cellphonedb_app
from cellphonedb.src.local_launchers.local_method_launcher import LocalMethodLauncher
from cellphonedb.src.tests.cellphone_flask_test_case import CellphoneFlaskTestCase
from cellphonedb.utils import dataframe_functions


class TestTerminalMethodStatisticalAnalysis(CellphoneFlaskTestCase):
    def create_app(self):
        return create_app(raise_non_defined_vars=False, verbose=True)

    def test_test_data__it_10__seed_0__threshold__01__precision_1(self):
        iterations = 10
        data = 'test'
        debug_seed = 0
        project_name = 'test_data'
        threshold = 0.1
        result_precision = 1
        self._method_call(data, iterations, project_name, threshold, debug_seed, result_precision)

    def test_test_data__it_10__seed_0__threshold__01__precision_3(self):
        iterations = 10
        data = 'test'
        debug_seed = 0
        project_name = 'test_data'
        threshold = 0.1
        result_precision = 3
        self._method_call(data, iterations, project_name, threshold, debug_seed, result_precision)

    def _method_call(self,
                     data: str,
                     iterations: int,
                     project_name: str,
                     threshold: float,
                     debug_seed: int,
                     result_precision: int):
        result_means_filename = self._get_result_filename('means', data, iterations, debug_seed, threshold,
                                                          result_precision)
        result_pvalues_filename = self._get_result_filename('pvalues', data, iterations, debug_seed, threshold,
                                                            result_precision)
        result_significant_means_filename = self._get_result_filename('significant_means', data, iterations, debug_seed,
                                                                      threshold, result_precision)
        result_pvalues_means_filename = self._get_result_filename('pvalues_means', data, iterations, debug_seed,
                                                                  threshold, result_precision)
        result_deconvoluted_filename = self._get_result_filename('deconvoluted', data, iterations, debug_seed,
                                                                 threshold, result_precision)

        meta_filename = os.path.realpath('{}/hi_{}_meta.txt'.format(data_test_dir, data))
        counts_filename = os.path.realpath('{}/hi_{}_counts.txt'.format(data_test_dir, data))

        LocalMethodLauncher(cellphonedb_app.cellphonedb). \
            cpdb_statistical_analysis_local_method_launcher(meta_filename,
                                                            counts_filename,
                                                            project_name,
                                                            iterations,
                                                            threshold,
                                                            output_test_dir,
                                                            result_means_filename,
                                                            result_pvalues_filename,
                                                            result_significant_means_filename,
                                                            result_pvalues_means_filename,
                                                            result_deconvoluted_filename,
                                                            debug_seed,
                                                            result_precision=result_precision)

        self._assert_result('means', data, iterations, project_name, result_means_filename, debug_seed, threshold,
                            result_precision)
        self._assert_result('pvalues', data, iterations, project_name, result_pvalues_filename, debug_seed, threshold,
                            result_precision)
        self._assert_result('significant_means', data, iterations, project_name, result_significant_means_filename,
                            debug_seed, threshold, result_precision)
        self._assert_result('pvalues_means', data, iterations, project_name, result_pvalues_means_filename, debug_seed,
                            threshold, result_precision)
        self._assert_result('deconvoluted', data, iterations, project_name, result_deconvoluted_filename, debug_seed,
                            threshold, result_precision)

    def _assert_result(self, filename: str,
                       data: str,
                       iterations: int,
                       project_name: str,
                       result_means_filename: str,
                       debug_seed: int,
                       threshold: float,
                       result_precision: int
                       ) -> None:
        str_threshold = ''.join(str(threshold).split('.'))

        means_test_filename = \
            'statistical_analysis__{}_result__' \
            'data-{}_it-{}_seed-{}_threshold-{}_precision-{}.txt'.format(filename,
                                                                         data,
                                                                         iterations,
                                                                         debug_seed,
                                                                         str_threshold,
                                                                         result_precision)
        original_means = pd.read_table(os.path.realpath('{}/{}'.format(data_test_dir, means_test_filename)))
        result_means = pd.read_table('{}/{}/{}'.format(output_test_dir, project_name, result_means_filename))
        self.assertTrue(dataframe_functions.dataframes_has_same_data(result_means, original_means))
        self.remove_file('{}/{}/{}'.format(output_test_dir, project_name, result_means_filename))

    def _get_result_filename(self,
                             base_name,
                             data: str,
                             iterations: int,
                             debug_seed: int,
                             threshold: float,
                             precision: int
                             ) -> str:
        str_threshold = ''.join(str(threshold).split('.'))

        base_filename = '{}__data-{}_it-{}_seed-{}_threshold-{}_precision-{}'.format(base_name,
                                                                                     data,
                                                                                     iterations,
                                                                                     debug_seed,
                                                                                     str_threshold,
                                                                                     precision)
        random_filename = self.get_test_filename(base_filename, 'txt')

        return random_filename
