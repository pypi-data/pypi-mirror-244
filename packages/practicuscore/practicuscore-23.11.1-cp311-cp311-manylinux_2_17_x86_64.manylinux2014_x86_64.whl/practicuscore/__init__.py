from typing import Optional, List, Union, TYPE_CHECKING
from practicuscore.profiler import Profiler

if TYPE_CHECKING:
    from practicuscore.api_def import ModelSearchResults, ModelConfig
    import pandas.core.frame
    # noinspection PyUnresolvedReferences
    import dask.dataframe.core
    # noinspection PyUnresolvedReferences
    import cudf.core.dataframe
    # noinspection PyUnresolvedReferences
    import dask_cudf.core
    # noinspection PyUnresolvedReferences
    import pyspark.pandas.frame

__version__ = '23.11.1'


class DataPipeline:
    def __init__(self, df: Optional[Union['pandas.core.frame.DataFrame', 'dask.dataframe.core.DataFrame',
                                          'cudf.core.dataframe.DataFrame', 'dask_cudf.core.DataFrame',
                                          'pyspark.pandas.frame.DataFrame']] = None):
        """
        Initializes DataPrep engine
        :param df: (Optional) Pandas, DASK, RAPIDS (cudf), RAPIDS+DASK for multi GPU (dask_cudf) or Spark (pandas compatible) dataframe
        """
        from practicuscore.dpi import DataPipelineInternal

        self.dpi = DataPipelineInternal(df)

    @staticmethod
    def from_config(cloud_worker_config: dict) -> 'DataPipeline':
        dp = DataPipeline()
        _ = dp.dpi.connect_to_node(cloud_worker_config)
        return dp

    def reset_steps(self, *args, **kwargs):
        self.dpi.reset_recorded_steps()

    def show_steps(self, *args, **kwargs):
        self.dpi.show_recorded_steps()

    def save_worksheet(
            self,
            file_path: str,
            sampling_method: Optional[str] = "TOP",
            sample_size: Optional[int] = 1000,
            *args, **kwargs):
        from practicuscore.core_def import CoreDef
        if not file_path.endswith(CoreDef.APP_FILE_TYPE):
            file_path += CoreDef.APP_FILE_TYPE
        if sampling_method is not None:
            sampling_message = f"A sample of {sampling_method} {sample_size} rows are included"
        else:
            sampling_message = "No sample included. \nPlease consider using dp.save_worksheet(file_path, " \
                               "sample_df=df, sample_size=100) to include 100 samples of the dataframe in the saved " \
                               "worksheet "
        self.dpi.save_ws(file_path, sampling_method, sample_size)
        print(f"Worksheet saved to {file_path}. {sampling_message}")

    def run_steps(self, *args, **kwargs):
        self.dpi.run_recorded_steps()

    def get_activity_log(self, *args, **kwargs):
        return self.dpi.get_ws_activity_log()

    def show_activity_log(self, *args, **kwargs):
        print("Activity Log:")
        print(self.dpi.get_ws_activity_log())

    def get_cloud_worker_issues(self, *args, **kwargs):
        return self.dpi.async_op_issue_list

    def show_cloud_worker_issues(self, *args, **kwargs):
        if self.dpi.using_node:
            if len(self.dpi.async_op_issue_list) > 0:
                print("\nCloud Worker (backend) issues:")
                for op_result in self.dpi.async_op_issue_list:
                    print(op_result)
        else:
            print("Not using Cloud Workers")

    def show_history(self, *args, **kwargs):
        self.show_activity_log()
        if self.dpi.using_node:
            self.wait_until_ws_is_free(1)
            self.show_cloud_worker_issues()

    def delete_steps(self, *args, **kwargs):
        self.dpi.delete_recorded_steps(*args)

    def delete_columns(self, column_list: List[str], *args, **kwargs):
        """
        Deletes columns from the DataFrame
        :param column_list: Column list to delete
        """
        self.dpi.delete_columns(column_list)

    def rename_column(self, from_column_name: str, to_column_name: str, *args, **kwargs):
        """
        Renames a columns with inplace editing
        :param from_column_name: Existing column name
        :param to_column_name: New column name
        :return: None
        """
        self.dpi.rename_column(from_column_name, to_column_name)

    def rename_columns(self, columns_dict: dict, *args, **kwargs):
        """
        Renames a columns with inplace editing
        :param columns_dict: A dictionary containing old and new column names(s)
        :return: None
        """
        self.dpi.rename_columns(columns_dict)

    def change_column_type(self, column_name: str, column_type: str, *args, **kwargs):
        """
        Changes column data type
        :param column_name: Column name to change
        :param column_type: Column Type- Text, Numeric, Date Time, Boolean
        :return: None
        """
        self.dpi.change_column_type(column_name, column_type)

    def filter(self, filter_expression: str, *args, **kwargs):
        """
        Filter on column
        :param filter_expression: Filter expression on column
        :return: None
        """
        self.dpi.filter(filter_expression)

    def one_hot_encode(self, column_name: str, column_prefix: str, *args, **kwargs):
        """
        One hot encoding on data
        :param column_name: Column name to one hot encoding
        :param column_prefix: Column prefix for one hot encoding
        :return: None
        """
        self.dpi.one_hot(column_name, column_prefix)

    def categorical_map(self, column_name: str, column_suffix: str, *args, **kwargs):
        """
        Categorical mapping on data
        :param column_name: Column name to categorical map
        :param column_suffix: Column prefix for categorical mapping
        :return: None
        """
        self.dpi.categorical_map(column_name, column_suffix)

    def split_column(self, column_name: str, split_using: str, *args, **kwargs):
        """
        Split column data
        :param column_name: Column name to split
        :param split_using: Column prefix for split
        :return: None
        """
        self.dpi.split_column(column_name, split_using)

    def handle_missing(self, technique: str, column_list: List[str], custom_value: str, *args, **kwargs):
        """
        Handle missing values on column
        :param technique: Handle missing technique
        :param column_list: Column list to handle missing values
        :param custom_value: Value for replace to missing values
        :return: None
        """
        self.dpi.handle_missing(technique, column_list, custom_value)

    def sort(self, column_list: List[str], ascending: List[bool], *args, **kwargs):
        """
        Sort on column
        :param column_list: Column list to sort
        :param ascending: True or False for ascending or descending order
        :return: None
        """
        self.dpi.sort_column(column_list, ascending)

    def group_by(self, columns: List[str], aggregation: dict, *args, **kwargs):
        """
        Group by column
        :param columns: Column list to group by
        :param aggregation: Column to group with technique
        :return: None
        """
        self.dpi.group_by_column(columns, aggregation)

    def time_sample(self, date_column: str, summary_column: str, summary_method: str, frequency: str, *args, **kwargs):
        """
        Time sample summarization
        :param date_column: Date column to calculate time sample summary for
        :param summary_column: Numeric column to calculate the summary
        :param summary_method: Aggregation (mean, sum etc) method
        :param frequency: D, M (Day, month etc.) frequency value. Uses Pandas standard
        :return: None
        """
        self.dpi.time_sample(date_column, summary_column, summary_method, frequency)

    def update_values(self, column_name: str, old_value: str, new_value: str, *args, **kwargs):
        """
        Updates column values to new values
        :param column_name: Column name to update
        :param old_value: Values in column to be update
        :param new_value: New value for update
        :return: None
        """
        self.dpi.update_values(column_name, old_value, new_value)

    def run_formula(self, new_column_name: str, formula_expression: str, *args, **kwargs):
        """
        Run formula with expression
        :param new_column_name: New Column name after formula applied
        :param formula_expression: Formula expression with selected Column
        :return: None
        """
        self.dpi.run_formula(new_column_name, formula_expression)

    def run_code(self, custom_function, *args, **kwargs):
        self.dpi.run_custom_code(custom_function)

    def run_sql(self, sql_query: str, sql_table_name: str, *args, **kwargs):
        self.dpi.run_custom_sql(sql_query, sql_table_name)

    def register_udf(self, udf, *args, **kwargs):
        self.dpi.register_udf_code(udf)

    def build_model(
            self,
            model_conf_file: Optional[str] = None,
            model_conf_json: Optional[str] = None,
            timeout_min=300,
            *args, **kwargs) -> Optional['ModelConfig']:
        """
        Builds AI model.
        :param model_conf_file: (Optional) Model configuration file, explaining how the model should be built.
        :param model_conf_json: (Optional) Model configuration as json string.
        :param timeout_min: Time out in minutes. Default is 300 minutes
        :return: ModelConfig. Details of the resulting model.
        """
        return self.dpi.build_model(model_conf_file, model_conf_json, timeout_min)

    def register_model(self, *args, **kwargs):
        """
        Registers final AI model.
        :return: None
        """
        self.dpi.register_model()

    def find_model(self, model_text: str, *args, **kwargs) -> Optional['ModelSearchResults']:
        return self.dpi.find_model(model_text)

    def get_auth_token(self, host_url: str, email: str, password: str, *args, **kwargs) -> str:
        return self.dpi.get_auth_token(host_url, email, password)

    def deploy_model(
            self,
            host_url: str,
            email: str,
            auth_token: str,
            deployment_key: str,
            prefix: str,
            model_name: str,
            model_dir: Optional[str] = None,
            *args, **kwargs):
        self.dpi.deploy_model(
            host_url=host_url, email=email, auth_token=auth_token, deployment_key=deployment_key,
            prefix=prefix, model_name=model_name, model_dir=model_dir)

    def predict(
            self, api_url: str, model_id: int, api_token: Optional[str] = None,
            column_names: Optional[List[str]] = None, new_column_name: Optional[str] = None,
            batch_size: Optional[int] = None,
            compression_algo: Optional[str] = None,
            *args, **kwargs):
        self.dpi.predict(
            api_url=api_url, model_id=model_id, api_token=api_token,
            column_names=column_names, new_column_name=new_column_name,
            batch_size=batch_size,
            compression_algo=compression_algo)

    def predict_with_offline_model(
            self, column_names: Optional[List[str]] = None, new_column_name: Optional[str] = None,
            future_horizon: Optional[int] = None,
            mlflow_tracking_uri: Optional[str] = None, mlflow_model_uri: Optional[str] = None,
            model_conf_path: Optional[str] = None, model_conf: Optional[str] = None,
            problem_type: Optional[str] = None,
            *args, **kwargs):
        self.dpi.predict_with_offline_model(
            column_names=column_names, new_column_name=new_column_name,
            future_horizon=future_horizon,
            mlflow_tracking_uri=mlflow_tracking_uri, mlflow_model_uri=mlflow_model_uri,
            model_conf_path=model_conf_path, model_conf=model_conf,
            problem_type=problem_type)

    def join(self, left_key_col_name: str, right_key_col_name: str,
             conn_conf_file: Optional[str] = None, conn_conf_json: Optional[str] = None, right_ws_name=None,
             join_technique="Left", suffix_for_overlap="_right", summary_column=False, *args, **kwargs):
        self.dpi.join(left_key_col_name=left_key_col_name, right_key_col_name=right_key_col_name,
                      conn_conf_file=conn_conf_file, conn_conf_json=conn_conf_json, right_ws_name=right_ws_name,
                      join_technique=join_technique, suffix_for_overlap=suffix_for_overlap, summary_column=summary_column)

    def wait_until_ws_is_free(self, timeout_min=600, *args, **kwargs):
        self.dpi.wait_until_ws_is_free(timeout_min)

    def get_df_copy(
            self,
            timeout_min=600,
            *args, **kwargs) -> Union['pandas.core.frame.DataFrame', 'dask.dataframe.core.DataFrame',
                                      'cudf.core.dataframe.DataFrame', 'dask_cudf.core.DataFrame',
                                      'pyspark.pandas.frame.DataFrame']:
        return self.dpi.get_df_copy(timeout_min)

    def load(
            self,
            conn_conf_file: Optional[str] = None,
            conn_conf_json: Optional[str] = None,
            engine="PANDAS",
            *args, **kwargs):
        if not self.dpi.using_node:
            raise ConnectionError("Cannot run load() since you are not using a Cloud Worker.\n"
                                  "To experiment without a Cloud Worker service, "
                                  "please use a local dataframe and pass a df to DataPipeline()")
        self.dpi.load(conn_conf_file, conn_conf_json, engine)

    def save(
            self,
            conn_conf_file: Optional[str] = None,
            conn_conf_json: Optional[str] = None,
            timeout_min=600,
            *args, **kwargs):
        self.dpi.save(conn_conf_file, conn_conf_json, timeout_min)

    def kill_worker(self, *args, **kwargs):
        self.dpi.kill_worker()

    def terminate_active_node(self):
        self.dpi.terminate_active_node()

    @staticmethod
    def get_cloud_data_pipeline(cloud_worker_config: dict) -> 'DataPipeline':
        dp = DataPipeline.from_config(cloud_worker_config)
        return dp

    @staticmethod
    def run_on_cloud_data_pipeline(
            cloud_worker_config: dict,
            runner_module: str):
        print('Starting to run_on_cloud_data_pipeline')
        assert runner_module is not None
        dp = None
        try:
            dp = DataPipeline.get_cloud_data_pipeline(cloud_worker_config)
            dp.run_all_steps(runner_module)
            df = dp.get_df_copy()
            print(df.head())
        except Exception as _ex:
            print(f"Exception : {_ex}")
            raise _ex
        finally:
            if dp is not None:
                dp.terminate_active_node()
                print('terminate successful')
            print('finished run_on_cloud_data_pipeline')

    def run_all_steps(self, runner_module: str):
        self.dpi.call_func(runner_module, "run_all_steps", self)


def test():
    print(f"You are using Practicus AI Core version {__version__}.\n"
          f"Please check https://practicus.ai for detailed usage instructions")
