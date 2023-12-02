from pymongo import MongoClient
from typing import Any, Dict, Optional


class MongoDBClient:
    def __init__(self, uri: str, db_name: str):
        """
        Initialize the MongoDB client.

        :param uri: MongoDB URI string.
        :param db_name: Name of the database to connect to.
        """
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.flows_collection = self.db.flows

    def create_flow(self, flow_document: Dict[str, Any]) -> Any:
        """
        Create a new flow document in the database.

        :param flow_document: The document to be inserted into the flows collection.
        :return: The ID of the inserted document.
        """
        return self.flows_collection.insert_one(flow_document).inserted_id

    def get_flow(self, flow_id: Any) -> Dict[str, Any]:
        """
        Retrieve a flow document by its ID.

        :param flow_id: The ID of the flow document to retrieve.
        :return: The flow document if found, otherwise None.
        """
        return self.flows_collection.find_one({"flow_id": flow_id})

    def update_flow(self, flow_id: Any, update_data: Dict[str, Any]) -> Any:
        """
        Update a flow document in the database.

        :param flow_id: The ID of the flow document to update.
        :param update_data: A dictionary containing the fields to update.
        :return: The result of the update operation.
        """
        return self.flows_collection.update_one(
            {"flow_id": flow_id}, {"$set": update_data}
        )

    def add_field_to_flow(self, flow_id: Any, key: str, value: Any) -> Any:
        """
        Add or update a key-value pair in a flow document.

        :param flow_id: The ID of the flow document to update.
        :param key: The key (field name) to be added or updated in the document.
        :param value: The value to set for the key.
        :return: The result of the update operation.
        """
        return self.flows_collection.update_one(
            {"flow_id": flow_id}, {"$set": {key: value}}
        )

    def get_field_by_key(self, flow_id: Any, key: str) -> Optional[Any]:
        """
        Retrieve a specific field value from a flow document based on the key.

        :param flow_id: The ID of the flow document to retrieve the field from.
        :param key: The key (field name) to retrieve from the document.
        :return: The value of the specified field, or None if the field doesn't exist or the document is not found.
        """
        projection = {key: 1, "_id": 0}
        document = self.flows_collection.find_one(
            {"flow_id": flow_id}, projection
        )

        if document and key in document:
            return document[key]
        return None
