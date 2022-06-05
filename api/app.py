import os
from flask import (Flask, request, jsonify)
from generate_proof import generate_proof

db_path = os.environ['DB_PATH'] if 'DB_PATH' in os.environ else "goerli.sql"
port = os.environ['APP_PORT'] if 'APP_PORT' in os.environ else 3000

app = Flask(__name__)

print(f"Starting app DB_PATH={db_path}, PORT={port} ...")

@app.route("/live", methods=["GET"])
def live():
    return jsonify(status="live")

@app.route("/generate_proof", methods=["POST"])
def handle_generate_proof():
    data = request.get_json()
    block_num = int(data.get("block"))
    contract_address = int(data.get("contract"), 16)
    var_name = data.get("variable")

    (root_hash, storage_root,  merkleb_high, merkleb_low) = generate_proof(db_path, block_num, contract_address, var_name)
    return jsonify(
        root_hash=root_hash,
        storage_root=storage_root,
        merkleb_high=merkleb_high,
        merkleb_low=merkleb_low)

if __name__ == '__main__':
      app.run(host='0.0.0.0', port=port)