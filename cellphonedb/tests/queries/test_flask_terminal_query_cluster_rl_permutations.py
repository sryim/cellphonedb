from cellphonedb.flask_app import create_app, data_test_dir, output_test_dir
from cellphonedb.flask_terminal_query_launcher import FlaskTerminalQueryLauncher
from cellphonedb.tests.cellphone_flask_test_case import CellphoneFlaskTestCase


class TestHumanInteractionsPermutations(CellphoneFlaskTestCase):
    def create_app(self):
        return create_app(raise_non_defined_vars=False)

    # TODO: remove after refactor
    # def test_real_data(self):
    #     iterations = 2
    #     data = 'original_prefiltered'
    #     debug_seed = '0'
    #
    #     self.query_call(data, iterations, debug_seed)

    def test_test_data(self):
        iterations = '10'
        data = 'test'
        debug_seed = '0'
        self.query_call(data, iterations, debug_seed)

    def test_manual_data(self):
        iterations = '10'
        data = 'manual'
        debug_seed = '0'
        self.query_call(data, iterations, debug_seed)

    def test_manual_2_data(self):
        iterations = '10'
        data = 'manual_2'
        debug_seed = '0'
        self.query_call(data, iterations, debug_seed)

    def query_call(self, data, iterations, debug_seed: str):
        means_base_name = 'simple_means__data-{}_it-{}'.format(data, iterations)
        pvalues_base_name = 'simple_pvalues__data-{}_it-{}'.format(data, iterations)
        pvalues_means_base_name = 'simple_pvalues_means__data-{}_it-{}'.format(data, iterations)
        result_means_namefile = self.get_test_namefile(means_base_name, 'txt')
        result_pvalues_namefile = self.get_test_namefile(pvalues_base_name, 'txt')
        result_pvalues_means_namefile = self.get_test_namefile(pvalues_means_base_name, 'txt')

        meta_namefile = 'hi_{}_meta.txt'.format(data)
        counts_namefile = 'hi_{}_counts.txt'.format(data)

        FlaskTerminalQueryLauncher().cluster_rl_permutations(meta_namefile, counts_namefile, iterations, data_test_dir,
                                                             output_test_dir, result_means_namefile,
                                                             result_pvalues_namefile, result_pvalues_means_namefile,
                                                             debug_seed)

        # TODO: incomplete

        # means_test_namefile = 'hi_r_m_means__data-{}_it-{}.txt'.format(data, iterations)
        # original_means = pd.read_table('{}/{}'.format(data_test_dir, means_test_namefile))
        # result_means = pd.read_table('{}/{}'.format(output_test_dir, result_means_namefile))
        #
        # pvalues_test_namefile = 'hi_r_m_pvalues__data-{}_it-{}.txt'.format(data, iterations)
        # original_pvalues = pd.read_table('{}/{}'.format(data_test_dir, pvalues_test_namefile))
        # result_pvalues = pd.read_table('{}/{}'.format(output_test_dir, result_pvalues_namefile))
        #
        # self.assertTrue(dataframe_functions.dataframes_has_same_data(result_means, original_means))
        # self.assertTrue(dataframe_functions.dataframes_has_same_data(result_pvalues, original_pvalues))
        #
        # self.remove_file('{}/{}'.format(output_test_dir, result_means_namefile))
        # self.remove_file('{}/{}'.format(output_test_dir, result_pvalues_namefile))
