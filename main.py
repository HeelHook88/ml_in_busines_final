import dill
import pandas as pd
import os

from flask import request, jsonify

dill._dill._reverse_typemap['ClassType'] = type
# import cloudpickle
import flask
import logging
from logging.handlers import RotatingFileHandler

from time import strftime

app = flask.Flask(__name__)

handler = RotatingFileHandler(filename='./logs/app.log', maxBytes=100000, backupCount=10)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(handler)

model_path = "./models/lightgbm_pipeline.dill"
with open(model_path, 'rb') as f:
    model = dill.load(f)


@app.route("/", methods=["GET"])
def general():
    return """Welcome to fraudelent prediction process. Please use 'http://<address>/predict' to POST!!!"""


# функция POST запроса
@app.route("/predict", methods=["POST"])
def predict():
    data = {"success": False}
    dt = strftime("[%Y-%b-%d %H:%M:%S]")

    Age, BMI, Glucose, Insulin, HOMA, Leptin, Adiponectin, Resistin, MCP_1 = "", "", "", "", "", "", "", "", ""

    request_json = request.get_json()

    if request_json["Age"]:
        Age = request_json['Age']

    if request_json["BMI"]:
        BMI = request_json['BMI']

    if request_json["Glucose"]:
        Glucose = request_json['Glucose']

    if request_json["Insulin"]:
        Insulin = request_json['Insulin']

    if request_json["HOMA"]:
        HOMA = request_json['HOMA']

    if request_json["Leptin"]:
        Leptin = request_json['Leptin']

    if request_json["Adiponectin"]:
        Adiponectin = request_json['Adiponectin']

    if request_json["Resistin"]:
        Resistin = request_json['Resistin']

    if request_json["MCP_1"]:
        MCP_1 = request_json['MCP_1']


    logger.info(f'{dt} Data: Age={Age}, BMI={BMI}, \
                            Glucose={Glucose}, Insulin={Insulin}, HOMA={HOMA}, \
                            Leptin={Leptin}, Adiponectin={Adiponectin}, Resistin={Resistin},\
                            MCP_1={MCP_1}')
    try:
        preds = model.predict_proba(pd.DataFrame({'Age': [Age],
                                                    'BMI': [BMI],
                                                    'Glucose': [Glucose],
                                                    'Insulin': [Insulin],
                                                    'HOMA': [HOMA],
                                                    'Leptin': [Leptin],
                                                    'Adiponectin': [Adiponectin],
                                                    'Resistin': [Resistin],
                                                    'MCP_1': [MCP_1]
                                                  }))
    except AttributeError as e:
        logger.warning(f'{dt} Exception: {str(e)}')
        data['predictions'] = str(e)
        data['success'] = False
        return flask.jsonify(data)

    data["predictions"] = preds[:, 1][0]
    # indicate that the request was a success
    data["success"] = True

    # return the data dictionary as a JSON response


    return flask.jsonify(data)

# if this is the main thread of execution first load the model and
# then start the server



if __name__ == "__main__":
    print(("* Loading the model and Flask starting server..."
           "please wait until server has fully started"))
    port = int(os.environ.get('PORT', 8180))
    app.run(host='127.0.0.1', debug=True, port=port)
