import os

import pandas as pd
from neptunemapfre.client import AteneaRun
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from usecaseutils.data import (
    read_s3_parquet_folder_to_pandas,
    write_pandas_into_s3,
)
from usecaseutils.logger import preprocess_logger as logger

if __name__ == "__main__":
    dataproduct_neptune_run = AteneaRun()

    use_datalake_pro_bucket = False
    if use_datalake_pro_bucket:
        datalake_bucket = os.getenv('BUCKET_DATALAKE_PRO')
    else:
        datalake_bucket = os.getenv('BUCKET_DATALAKE')

    logger.info('Datalake bucket: ' + datalake_bucket)

    df = read_s3_parquet_folder_to_pandas(
        s3_bucket=datalake_bucket,
        parquet_folder='atenea_statistics/onprem_stats',
    )

    df.drop(
        [
            'stat_val',
            'filter',
        ],
        axis=1
    )

    categorical_vars = [
        'database_name',
        'table_name',
        'stat_id',
        'group',
    ]

    df[categorical_vars] = df[categorical_vars].apply(lambda x: pd.factorize(x)[0])

    X = df.drop(
        [
            'stat_val',
            'filter',
        ],
        axis=1
    )
    y = df['stat_val']

    logger.info('Splitting train and test data')
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

    sc = StandardScaler()
    X_train2 = pd.DataFrame(sc.fit_transform(X_train))
    X_test2 = pd.DataFrame(sc.transform(X_test))
    X_train2.columns = X_train.columns.values
    X_test2.columns = X_test.columns.values
    X_train2.index = X_train.index.values
    X_test2.index = X_test.index.values
    X_train = X_train2
    X_test = X_test2

    # Save preprocess data

    output_bucket = os.getenv('BUCKET_DATAPRODUCT')
    processed_folder = 'data/processed'

    logger.info(f"Saving data into output bucket: {output_bucket}/{processed_folder}")

    # X TRAIN
    x_train_file = f'{processed_folder}/x_train.csv'

    write_pandas_into_s3(
        dataframe=X_train,
        s3_bucket=output_bucket,
        filename=x_train_file,
        sep=','
    )

    dataproduct_neptune_run.track_data(
        dataset_path=f'{output_bucket}/{x_train_file}',
        key=x_train_file,
    )

    # X TEST
    x_test_file = f'{processed_folder}/x_test.csv'

    write_pandas_into_s3(
        dataframe=X_test,
        s3_bucket=output_bucket,
        filename=x_test_file,
        sep=','
    )

    dataproduct_neptune_run.track_data(
        dataset_path=f'{output_bucket}/{x_test_file}',
        key=x_test_file,
    )

    # Y TRAIN
    y_train_file = f'{processed_folder}/y_train.csv'

    write_pandas_into_s3(
        dataframe=y_train,
        s3_bucket=output_bucket,
        filename=y_train_file,
        sep=','
    )

    dataproduct_neptune_run.track_data(
        dataset_path=f'{output_bucket}/{y_train_file}',
        key=y_train_file,
    )

    # Y TEST
    y_test_file = f'{processed_folder}/y_test.csv'

    write_pandas_into_s3(
        dataframe=y_test,
        s3_bucket=output_bucket,
        filename=y_test_file,
        sep=','
    )

    dataproduct_neptune_run.track_data(
        dataset_path=f'{output_bucket}/{y_test_file}',
        key=y_test_file,
    )

    logger.info("Saving data completed")
