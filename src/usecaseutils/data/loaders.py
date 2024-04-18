import logging
import pickle

import awswrangler as wr
import pandas as pd
from cloudpathlib import CloudPath

__data_logger = logging.getLogger('data')


def __remove_final_slash_bucket(
        s3_bucket: str,
):
    return s3_bucket[:-1] if s3_bucket.endswith('/') else s3_bucket


def execute_query_athena(
    query: str,
    database: str,
    athena_output_location: str,
    **kwargs
):
    # https://aws-sdk-pandas.readthedocs.io/en/stable/stubs/awswrangler.athena.start_query_execution.html
    return wr.athena.start_query_execution(
        sql=query,
        database=database,
        s3_output=athena_output_location,
        **kwargs
    )


def read_athena_to_pandas(
        query: str,
        database: str,
        athena_output_location: str,
        **kwargs
):
    # https://aws-sdk-pandas.readthedocs.io/en/stable/stubs/awswrangler.athena.read_sql_query.html
    return wr.athena.read_sql_query(
        sql=query,
        database=database,
        s3_output=athena_output_location,
        ctas_approach=False,
        **kwargs
    )


def read_s3_to_pickle(
        s3_bucket: str,
        filename: str,
        **kwargs
):
    s3_bucket = __remove_final_slash_bucket(s3_bucket)

    with CloudPath(f'{s3_bucket}/{filename}').open('rb') as f:
        return pickle.load(
            f,
            **kwargs
        )


def read_s3_to_pandas(
        s3_bucket: str,
        filename: str,
        **kwargs
):
    s3_bucket = __remove_final_slash_bucket(s3_bucket)

    s3_input = f'{s3_bucket}/{filename}'
    __data_logger.debug(f'Reading data from: {s3_input}')
    return pd.read_csv(
        CloudPath(s3_input),
        **kwargs
    )


def read_s3_parquet_folder_to_pandas(
        s3_bucket: str,
        parquet_folder: str,
        **kwargs
):
    s3_bucket = __remove_final_slash_bucket(s3_bucket)

    s3_input = f'{s3_bucket}/{parquet_folder}/'
    __data_logger.debug(f'Reading parquet from: {s3_input}')
    return wr.s3.read_parquet(
        [
            str(parquet_path) for parquet_path in list(
            CloudPath(s3_input).glob(
                '**/*.parquet'
            ))
        ],
        **kwargs
    )


def write_pickle_into_s3(
        pickle_object: object,
        s3_bucket: str,
        filename: str,
        **kwargs
):
    s3_bucket = __remove_final_slash_bucket(s3_bucket)

    with CloudPath(f's3://{s3_bucket}/{filename}').open('wb') as f:
        pickle.dump(
            pickle_object,
            f,
            **kwargs
        )


def write_pandas_into_s3(
        dataframe: pd.DataFrame,
        s3_bucket: str,
        filename: str,
        **kwargs
):
    s3_bucket = __remove_final_slash_bucket(s3_bucket)

    s3_out = f'{s3_bucket}/{filename}'
    __data_logger.debug(f'writing training data to {s3_out}')
    with CloudPath(s3_out).open('w') as f:
        dataframe.to_csv(
            f,
            index=False,
            **kwargs
        )

    __data_logger.debug(f'Data saved in {s3_out}')
