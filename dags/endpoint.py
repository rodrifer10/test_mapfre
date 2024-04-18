# Generic imports
import json
from datetime import datetime

# Airflow imports
from airflow import DAG
from airflowmapfre.providers.mapfre.config.runtime import (
    AteneaBatchImages,
    AteneaEndpointImages,
    AteneaRuntimeSagemakerEndpointSize,
    AteneaRuntimeSagemakerJobSize,
)
from airflowmapfre.providers.mapfre.operators.mlops.sagemaker import (
    AteneaSageMakerEndpointOperator,
    AteneaSageMakerProcessingOperator,
)
from airflowmapfre.providers.mapfre.utils.airflow import get_uuid_tag

# DAG metadata
DAG_OWNERS = 'epgonz1@mapfre.com'
DAG_MAILING_LIST = 'epgonz1@mapfre.com'

REPO_URL = 'https://bitbucket.org/ateneadataproducts/apps-mlops-dataproduct-testing-ep.git'
dag_tags = ['ml', 'testing-ep', 'https://bitbucket.org/ateneadataproducts/apps-mlops-dataproduct-testing-ep.git', 'adp', 'adp']


# If removed DAG and AWS job mapping would be more difficult
DAG_NAME = 'adp-ml-testing-ep-templated'
dag_tags.append(
    get_uuid_tag(DAG_NAME)
)


PROJECT_NAME = 'apps-mlops-dataproduct-testing-ep'

DAG_DOC = '''
# DAG Documentation
## apps-mlops-dataproduct-testing-ep

,
'''

# Execution common arguments
CODE_BRANCH = 'develop'  # Just an example <YOUR_CODE_BRANCH_HERE>
CODE_BASE_PATH = 'src'
REQUIREMENTS_BASE_PATH = 'requirements.txt'

# define airflow DAG
default_args = {
    'owner': DAG_OWNERS,
    'email': DAG_MAILING_LIST.split(','),
}

with DAG(
        dag_id=DAG_NAME,
        default_args=default_args,
        # max_active_tasks=1, # limit task concurrency
        # max_active_runs=1, # limit dag concurrency
        # Set your schedule interval: https://airflow.apache.org/docs/apache-airflow/2.2.2/dag-run.html#cron-presets
        schedule=None,
        start_date=datetime(2021, 1, 1),
        user_defined_filters={'tojson': lambda s: json.JSONEncoder().encode(s)},
        tags=dag_tags,
        doc_md=DAG_DOC,
) as dag:
    preprocess_task = AteneaSageMakerProcessingOperator(
        task_id='preprocess',
        runtime_image=AteneaBatchImages.latest_PYTHON_3_9_12,
        runtime_size=AteneaRuntimeSagemakerJobSize.MEDIUM_MEDIUM_MEMORY,
        repo_url=REPO_URL,
        repo_branch=CODE_BRANCH,
        script_path=f'{CODE_BASE_PATH}/preprocess.py',
        script_requirements_path=REQUIREMENTS_BASE_PATH,
        neptune_project=PROJECT_NAME,
    )

    training_task = AteneaSageMakerProcessingOperator(
        task_id='training',
        runtime_image=AteneaBatchImages.latest_PYTHON_3_9_12,
        runtime_size=AteneaRuntimeSagemakerJobSize.MEDIUM_MEDIUM_MEMORY,
        repo_url=REPO_URL,
        repo_branch=CODE_BRANCH,
        script_path=f'{CODE_BASE_PATH}/training.py',
        script_requirements_path=REQUIREMENTS_BASE_PATH,
        neptune_project=PROJECT_NAME,
    )

    deploy_task = AteneaSageMakerEndpointOperator(
        task_id="deploy",
        runtime_image=AteneaEndpointImages.latest_PYTHON_3_9_12,
        runtime_size=AteneaRuntimeSagemakerEndpointSize.MEDIUM_LOW_MEMORY,
        repo_url=REPO_URL,
        repo_branch=CODE_BRANCH,
        script_requirements_path=REQUIREMENTS_BASE_PATH,
        neptune_project=PROJECT_NAME,
        data_capture=True,
    )
    preprocess_task >> training_task >> deploy_task
