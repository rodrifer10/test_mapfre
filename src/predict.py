from neptunemapfre.client import AteneaModel
import numpy as np

def load_model():
    global model
    dataproduct_neptune_model = AteneaModel(
        model_id='LOGREG',
        model_name='Cookiecutter Templated'
    )
    model_version = dataproduct_neptune_model.model_version(
        retrieve_key='LAST'
    )
    model = model_version.download_pickle()


def predict(input_data):
    input_data = np.array(list(input_data["features"].values())).reshape(1, -1)
    y_pred = model.predict(input_data)
    status_code = "200"
    return y_pred.tolist(), status_code
