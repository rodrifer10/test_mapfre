import os

import neptune.integrations.sklearn as npt_utils
from neptunemapfre.client import (
    AteneaModel,
    AteneaRun,
)
from sklearn.linear_model import LogisticRegression

from usecaseutils.data import read_s3_to_pandas
from usecaseutils.logger import training_logger as logger

if __name__ == '__main__':
    dataproduct_neptune_run = AteneaRun()
    dataproduct_neptune_model = AteneaModel(
        model_id='LOGREG',
        model_name='Cookiecutter Templated'
    )

    output_bucket = os.getenv('BUCKET_DATAPRODUCT')
    processed_folder = 'data/processed'

    logger.info(f"Reading data from: {output_bucket}/{processed_folder}")

    X_train = read_s3_to_pandas(
        s3_bucket=output_bucket,
        filename=f'{processed_folder}/x_train.csv',
        sep=',',
    )

    y_train = read_s3_to_pandas(
        s3_bucket=output_bucket,
        filename=f'{processed_folder}/y_train.csv',
        sep=',',
    )

    # Managing models with atenea-lib-neptune
    model_version = dataproduct_neptune_model.model_version()

    dataproduct_neptune_run.set_tag(
        value=['Training', 'Logistic Regression', 'Cookiecutter Templated']
    )

    # Doing data science

    logger.info("Training model initiated")

    parameters_run = {
        "random_state": 0,
        "penalty": 'l2'
    }

    classifier = LogisticRegression(**parameters_run)
    classifier.fit(X_train.tail(5), y_train.tail(5).values.ravel())
    dataproduct_neptune_run.set_params(
        value=npt_utils.get_estimator_params(classifier)
    )
    model_version.upload_pickle(classifier)

    logger.info("Training model completed")
