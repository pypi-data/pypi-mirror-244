import requests
from typing import Any, Dict

from python_sdk.colossus_exceptions import ColossusAPIError


class ColossusClient:
    """
    A client for interacting with the Colossus Staking API.

    Attributes:
        api_key (str): The API key used for authenticating with the Colossus API.
        base_url (str): The base URL of the Colossus API.
    """

    def __init__(
        self, api_key: str, base_url: str = "http://127.0.0.1:5000"
    ) -> None:
        """
        Initializes the ColossusClient with an API key and base URL.

        Args:
            api_key (str): The API key for Colossus API.
            base_url (str): The base URL for the Colossus API. Defaults to 'http://127.0.0.1:5000'.
        """
        self.api_key = api_key
        self.base_url = base_url

    def create_flow(self, flow_request: "FlowRequest") -> "FlowResponse":
        """
        Creates a new flow in the Colossus Staking API.

        Args:
            flow_request (FlowRequest): The flow request data.

        Returns:
            FlowResponse: The response from the API after creating the flow.

        Raises:
            ColossusAPIError: If the API request fails.
        """
        url = f"{self.base_url}/api/v1/flows"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        response = requests.post(
            url, json=flow_request.to_dict(), headers=headers
        )

        if response.status_code == 201:
            return FlowResponse.from_dict(response.json())
        else:
            raise ColossusAPIError(response.status_code, response.text)

    def submit_delegate_data(
        self, flow_id: str, delegate_data_request: "DelegateDataRequest"
    ) -> "FlowResponse":
        """
        Submits delegate data for a specified flow.

        Args:
            flow_id (str): The ID of the flow.
            delegate_data_request (DelegateDataRequest): The delegate data to be submitted.

        Returns:
            FlowResponse: The response from the API after submitting the delegate data.

        Raises:
            ColossusAPIError: If the API request fails.
        """
        url = f"{self.base_url}/api/v1/flows/{flow_id}"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        response = requests.put(
            url, json=delegate_data_request.to_dict(), headers=headers
        )

        if response.status_code == 200:
            return FlowResponse.from_dict(response.json())
        else:
            raise ColossusAPIError(response.status_code, response.text)

    def submit_signed_transaction(
        self, flow_id: str, transaction_request: "SubmitTransactionRequest"
    ) -> "FlowResponse":
        """
        Submits a signed delegate transaction for broadcasting in a specified flow.

        Args:
            flow_id (str): The ID of the flow.
            transaction_request (SubmitTransactionRequest): The signed transaction to be broadcast.

        Returns:
            FlowResponse: The response from the API after submitting the transaction.

        Raises:
            ColossusAPIError: If the API request fails.
        """
        url = f"{self.base_url}/api/v1/flows/{flow_id}/next"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        response = requests.put(
            url, json=transaction_request.to_dict(), headers=headers
        )

        if response.status_code == 200:
            return FlowResponse.from_dict(response.json())
        else:
            raise ColossusAPIError(response.status_code, response.text)


# Model Classes
class FlowRequest:
    """
    Represents a request to create a new flow in the Colossus Staking API.

    Attributes:
        network_code (str): Network code of the flow.
        chain_code (str): Chain code of the flow.
        operation (str): The operation to be performed in the flow.
    """

    def __init__(
        self, network_code: str, chain_code: str, operation: str
    ) -> None:
        """
        Initializes a FlowRequest instance.

        Args:
            network_code (str): Network code of the flow.
            chain_code (str): Chain code of the flow.
            operation (str): The operation to be performed in the flow.
        """
        self.network_code = network_code
        self.chain_code = chain_code
        self.operation = operation

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the FlowRequest instance to a dictionary.

        Returns:
            Dict[str, Any]: A dictionary representation of the FlowRequest instance.
        """
        return {
            "flow": {
                "network_code": self.network_code,
                "chain_code": self.chain_code,
                "operation": self.operation,
            }
        }


class FlowResponse:
    """
    Represents a response from the Colossus Staking API for a flow creation request.

    Attributes:
        id (str): The ID of the flow.
        operation (str): The operation being performed by the flow.
        state (str): The current state of the flow.
        actions (Any): The actions included in the flow response.
        data (Any): The data included in the flow response.
    """

    def __init__(self, id, operation, state, actions, data):
        """
        Initializes a FlowResponse instance with response data from the Colossus API.

        Args:
            id (str): The unique identifier for the flow.
            operation (str): The type of operation being performed in the flow.
            state (str): The current state of the flow.
            actions (Any): The next possible actions in the flow. The structure of this attribute
                           depends on the specific API response.
            data (Any): Additional data associated with the flow. The structure of this attribute
                        depends on the specific API response.
        """
        self.id = id
        self.operation = operation
        self.state = state
        self.actions = actions
        self.data = data

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "FlowResponse":
        """
        Constructs a FlowResponse object from a dictionary.

        Args:
            data (Dict[str, Any]): A dictionary containing flow response data.

        Returns:
            FlowResponse: An instance of FlowResponse constructed from the provided data.
        """
        return FlowResponse(
            id=data.get("id"),
            operation=data.get("operation"),
            state=data.get("state"),
            actions=data.get("actions"),
            data=data.get("data"),
        )


class DelegateDataRequest:
    """
    Represents a request for delegate data in the context of the Colossus API.

    Attributes:
        name (str): The name of the delegate operation.
        inputs (Dict[str, Any]): The input parameters for the delegate operation.
    """

    def __init__(self, name: str, inputs: Dict[str, Any]) -> None:
        """
        Initializes a new instance of DelegateDataRequest.

        Args:
            name (str): The name of the delegate operation.
            inputs (Dict[str, Any]): A dictionary of input parameters for the delegate operation.
        """
        self.name = name
        self.inputs = inputs

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the DelegateDataRequest instance to a dictionary.

        Returns:
            Dict[str, Any]: The dictionary representation of the request.
        """
        return self.inputs


class SubmitTransactionRequest:
    """
    Represents a request for submitting a signed transaction in the context of the Colossus API.

    Attributes:
        name (str): The name of the transaction operation, defaulting to "sign_delegate_tx".
        inputs (Dict[str, str]): Input parameters for the transaction, including the transaction payload.
        signatures (List[Dict[str, str]]): A list of signatures associated with the transaction.
    """

    def __init__(self, transaction_payload: str, signature_data: str) -> None:
        """
        Initializes a new instance of SubmitTransactionRequest.

        Args:
            transaction_payload (str): The payload of the signed transaction.
            signature_data (str): The signature data associated with the transaction.
        """
        self.name = "sign_delegate_tx"
        self.inputs = {"transaction_payload": transaction_payload}
        self.signatures = [{"signature_data": signature_data}]

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the SubmitTransactionRequest instance to a dictionary.

        Returns:
            Dict[str, Any]: The dictionary representation of the request, including name, inputs, and signatures.
        """
        return {
            "name": self.name,
            "inputs": self.inputs,
            "signatures": self.signatures,
        }
