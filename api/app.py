import os
from flask import (Flask, request, jsonify)
from generate_proof import generate_proof

db_path = ""

try:
    db_path = os.environ['DB_PATH']
except:
    print("Could not load DB_PATH env var")
    exit(1)

app = Flask(__name__)

@app.route("/generate_proof", methods=["POST"])
def hello_world():
    data = request.get_json()
    block_num = int(data.get("block"))
    contract_address = int(data.get("contract"), 16)
    var_name = int(data.get("variable"))

    (root_hash, storage_root,  merkleb_high, merkleb_low) = generate_proof(db_path, block_num, contract_address, var_name)
    return jsonify(
        root_hash=root_hash,
        storage_root=storage_root,
        merkleb_high=merkleb_high,
        merkleb_low=merkleb_low)