import logging

from .loaders import (
    execute_query_athena,
    read_athena_to_pandas,
    read_s3_parquet_folder_to_pandas,
    read_s3_to_pandas,
    read_s3_to_pickle,
    write_pandas_into_s3,
    write_pickle_into_s3,
)

__data_logger = logging.getLogger('data')
__data_logger.setLevel(logging.INFO)

__all__ = [
    'execute_query_athena',
    'read_athena_to_pandas',
    'read_s3_parquet_folder_to_pandas',
    'read_s3_to_pandas',
    'write_pandas_into_s3',
    'write_pickle_into_s3',
    'read_s3_to_pickle',
]
