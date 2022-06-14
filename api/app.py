import os
from flask import (Flask, request, jsonify)
from flask_cors import CORS, cross_origin
from generate_proof import generate_proof


db_path = os.environ['DB_PATH'] if 'DB_PATH' in os.environ else "goerli.sql"
port = os.environ['APP_PORT'] if 'APP_PORT' in os.environ else 3000

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

print(f"Starting app DB_PATH={db_path}, PORT={port} ...")


@app.route("/live", methods=["GET"])
def live():
    return jsonify(status="live")


@app.route("/generate_proof", methods=["POST"])
@cross_origin()
def handle_generate_proof():
    data = request.get_json()
    block_num = int(data.get("block"))
    contract_address = int(data.get("contract"), 16)
    var_name = data.get("variable")
    args = data.get("args")

    response = None

    try:
        (root_hash, storage_root,  merkleb_high, merkleb_low) = generate_proof(
            db_path, block_num, contract_address, var_name, *args)
        response = jsonify(
            root_hash=str(root_hash),
            storage_root=str(storage_root),
            merkleb_high=merkleb_high,
            merkleb_low=merkleb_low,
            error="")
    except AssertionError as e:
        response = jsonify(error=str(e))

    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)
