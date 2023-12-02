from colossus_client import (
    ColossusClient,
    FlowRequest,
    DelegateDataRequest,
    SubmitTransactionRequest,
)
from colossus_exceptions import ColossusAPIError

api_key = "your_api_key_here"
client = ColossusClient(api_key)

flow_request = FlowRequest(
    network_code="cosmos", chain_code="testnet", operation="staking"
)

try:
    # Create a new flow using the Colossus client and the flow request
    flow_response = client.create_flow(flow_request)
    print("Flow ID:", flow_response.id)
    # You can handle additional data from flow_response if needed

    # Prepare delegate data request with necessary information
    delegate_data_request = DelegateDataRequest(
        name="create_delegate_transaction",
        inputs={
            "delegator_address": "P-fuji1jpaykkzyaky3mgscflkgufmlnnrxa74cvn4z65",
            "validator_address": "NodeID-3VWnZNViBP2b56QBY7pNJSLzN2rkTyqnK",
            "amount": 10,
            "memo": "Optional memo text",  # This is an optional field
        },
    )

    # Submit delegate data to the specified flow and capture the response
    submit_delegate_data_response = client.submit_delegate_data(
        flow_response.id[0],
        delegate_data_request,  # Using the first flow ID from the response
    )
    print("Delegated State:", submit_delegate_data_response.state)

    # Create a transaction request with the signed transaction payload and signature data
    transaction_request = SubmitTransactionRequest(
        transaction_payload="sample_signed_transaction_payload",
        signature_data="sample_signature_data",
    )

    # Submit the signed transaction for the specified flow and capture the response
    submit_transaction_response = client.submit_signed_transaction(
        flow_response.id[0],
        transaction_request,  # Again, using the first flow ID from the response
    )
    print("Transaction State:", submit_transaction_response.state)

except ColossusAPIError as e:
    # Handle the Colossus API error here
    print("API error:", e)
