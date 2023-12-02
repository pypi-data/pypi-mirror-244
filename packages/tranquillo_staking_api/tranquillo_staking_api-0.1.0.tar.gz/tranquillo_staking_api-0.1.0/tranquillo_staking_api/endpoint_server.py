from flask import Flask, jsonify, request
import mongo_client
import uuid
from datetime import datetime
import json
from typing import Dict, Any, Optional


app = Flask(__name__)

# Initialize MongoDB client
mongodb_client = mongo_client.MongoDBClient(
    "mongodb://localhost:27017/", "staking"
)


# def store_flow_data_in_json(mongodb_client: MongoDBClient, flow_id: Any) -> Optional[str]:
def store_flow_data_in_json(flow_id: Any) -> Optional[str]:
    """
    Fetches a document with the specified flow_id from the MongoDB collection and stores it in a JSON structure.

    :param mongodb_client: An instance of the MongoDBClient.
    :param flow_id: The flow_id of the document to fetch.
    :return: A JSON string containing the data of the specified document, or None if the document doesn't exist.
    """
    document = mongodb_client.get_flow(flow_id)

    if document:
        # Convert the document to a JSON string
        return json.dumps(
            document, default=str
        )  # 'default=str' to handle ObjectId and datetime
    else:
        return None


def extract_value_from_json(json_data: str, key: str) -> Optional[Any]:
    """
    Extracts the value associated with the given key from the JSON string.

    :param json_data: A JSON string containing the data of a MongoDB document.
    :param key: The key whose value needs to be extracted from the JSON data.
    :return: The value associated with the specified key, or None if the key is not found or the JSON is invalid.
    """
    try:
        # Convert the JSON string to a dictionary
        data = json.loads(json_data)

        # Extract and return the value for the specified key
        return data.get(key)
    except json.JSONDecodeError:
        # Handle the case where json_data is not a valid JSON
        return None


def get_current_timestamp():
    """
    Generates the current timestamp in ISO 8601 format.

    Returns:
        str: The current timestamp as a string in ISO 8601 format.
    """
    return datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time


"""
curl -X POST -H "Content-Type: application/json" \
    -d '{
        "flow": 
        {
            "network_code": "cosmos", 
            "chain_code": "testnet", 
            "operation": "staking"
        }
    }' \
    http://127.0.0.1:5000/api/v1/flows
"""


@app.route("/api/v1/flows", methods=["POST"])
def create_staking_flow():
    data = request.json

    # Validate the data against the StakingFlow schema
    required_fields = ["network_code", "chain_code", "operation"]
    if not data.get("flow") or not all(
        field in data["flow"] for field in required_fields
    ):
        return jsonify({"error": "Invalid data provided"}), 400

    # If valid, process the data and create a new staking flow
    # This is a placeholder. You should replace it with actual logic to handle the staking flow creation.

    flow_id = (str(uuid.uuid4()),)  # Generate a unique ID for the flow
    updated_at = created_at = get_current_timestamp()

    # Create a document for the flow
    flow_document = {
        "flow_id": flow_id,
        "network_code": data["flow"]["network_code"],
        "chain_code": data["flow"]["chain_code"],
        "operation": data["flow"]["operation"],
        "created_at": created_at,
        "updated_at": updated_at,
        "state": "created",
    }

    # Store the document in MongoDB
    mongodb_client.create_flow(flow_document)

    # Mongodb commands
    # mongo
    # use staking
    # db.flows.find().pretty()
    # db.flows.find({"flow_id": "your_flow_id"}).pretty()
    # db.flows.find({"flow_id": "b2c4c9c9-a6ef-46f7-b1a4-e3aebd9ba84b"}).pretty()

    # Return the appropriate response
    response = {
        "id": flow_id,
        "operation": data["flow"]["operation"],
        "state": "initialized",
        "actions": [],  # You can populate this based on your logic
        "data": {},  # Placeholder for additional data related to the staking flow
        "network_code": data["flow"]["network_code"],
        "chain_code": data["flow"]["chain_code"],
        "created_at": created_at,  # Placeholder timestamp
        "updated_at": created_at,  # Placeholder timestamp
    }
    return jsonify(response), 201


"""
curl -X PUT -H "Content-Type: application/json" \
    -d '{
        "delegator_address": "cosmos1abcd1234",
        "validator_address": "cosmosvalidator1xyz7890",
        "amount": 100
    }' \
    http://127.0.0.1:5000/api/v1/flows/sample_flow_id
"""


@app.route("/api/v1/flows/<flow_id>", methods=["PUT"])
def delegate(flow_id):
    data = request.json

    # Validate the data against the DelegateRequest schema
    required_fields = ["delegator_address", "validator_address", "amount"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Invalid data provided"}), 400

    # Find the document with the given flow_id
    document = store_flow_data_in_json(flow_id)

    # Find the document with the given flow_id
    if document is None:
        return jsonify({"error": "flow id not found"}), 404

    # Verfiy the status
    if data.get("status") == "signed_delegate":
        return jsonify({"error": "flow state signed_delegate"}), 404

    # If valid, process the data and perform the delegation
    update_at = get_current_timestamp()

    # Update flow
    mongodb_client.update_flow(flow_id, {"updated_at": update_at})
    mongodb_client.update_flow(flow_id, {"state": "delegate"})
    mongodb_client.add_field_to_flow(
        flow_id, "delegator_address", data["delegator_address"]
    )
    mongodb_client.add_field_to_flow(
        flow_id, "validator_address", data["validator_address"]
    )
    mongodb_client.add_field_to_flow(flow_id, "amount", data["amount"])

    # Return the appropriate response
    response = {
        "id": flow_id,
        "operation": "delegation",
        "state": "delegated",
        "actions": [],  # You can populate this based on your logic
        "data": {
            "delegator_address": extract_value_from_json(
                document, "delegator_address"
            ),
            "validator_address": extract_value_from_json(
                document, "validator_address"
            ),
            "amount": data["amount"],
            # ... other fields from DelegateResponse schema
        },
        "network_code": extract_value_from_json(document, "network_code"),
        "chain_code": extract_value_from_json(document, "chain_code"),
    }
    return jsonify(response), 200


"""
curl -X PUT -H "Content-Type: application/json" \
-d '{
    "name": "sign_delegate_tx",
    "inputs": {
        "transaction_payload": "sample_signed_transaction_payload"
    },
    "signatures": [
        {
            "signature_data": "sample_signature_data"
        }
    ]
}' \
http://127.0.0.1:5000/api/v1/flows/sample_flow_id/next

"""


@app.route("/api/v1/flows/<flow_id>/next", methods=["PUT"])
def signed_delegate(flow_id):
    data = request.json

    # Validate the data
    if not data.get("name") == "sign_delegate_tx":
        return jsonify({"error": "Invalid operation name"}), 400

    if not data.get("inputs") or not data["inputs"].get("transaction_payload"):
        return jsonify({"error": "Missing transaction payload"}), 400

    if not data.get("signatures"):
        return jsonify({"error": "Missing signatures"}), 400

    # Find the document with the given flow_id
    document = store_flow_data_in_json(flow_id)

    # Find the document with the given flow_id
    if document is None:
        return jsonify({"error": "flow id not found"}), 404

    # If valid, process the data and perform the delegation
    update_at = get_current_timestamp()

    # Update flow
    mongodb_client.update_flow(flow_id, {"updated_at": update_at})
    mongodb_client.update_flow(flow_id, {"state": "signed_delegate"})
    mongodb_client.add_field_to_flow(flow_id, "signatures", data["signatures"])

    # Return the appropriate response
    response = {
        "id": flow_id,
        "operation": "sign_delegate_tx",
        "state": "broadcasted",
        "actions": [],  # You can populate this based on your logic
        "data": {
            "delegator_address": extract_value_from_json(
                document, "delegator_address"
            ),  # Placeholder
            "validator_address": extract_value_from_json(
                document, "validator_address"
            ),  # Placeholder
            "amount": extract_value_from_json(document, "amount"),
            "memo": "Sample memo",  # Placeholder
            "gas_price": "0.025",  # Placeholder
            "gas_limit": "200000",  # Placeholder
            "delegate_transaction": {
                "raw": "sample_raw_data",
                "signing_payload": data["inputs"]["transaction_payload"],
                "signed": data["signatures"][0]["signature_data"],
                "hash": "sample_hash",
                "status": "sample_status",
                "error": "sample_error",
                "signatures": data["signatures"],
                "block_time": "sample_block_time",
            },
            "pubkey": "sample_pubkey",
        },
        "network_code": extract_value_from_json(document, "network_code"),
        "chain_code": extract_value_from_json(document, "chain_code"),
        "created_at": extract_value_from_json(document, "created_at"),
        "updated_at": extract_value_from_json(document, "updated_at"),
    }
    return jsonify(response), 200


if __name__ == "__main__":
    app.run(debug=True)
