class ColossusAPIError(Exception):
    """
    A custom exception class for handling errors related to the Colossus API.

    Attributes:
        status_code (int): The HTTP status code associated with the API error.
    """

    def __init__(self, status_code: int, message: str) -> None:
        """
        Initializes the ColossusAPIError with a status code and an error message.

        Args:
            status_code (int): The HTTP status code associated with the error.
            message (str): A descriptive message of the error.
        """
        self.status_code = status_code
        super().__init__(message)

    def __str__(self) -> str:
        """
        Returns a string representation of the ColossusAPIError.

        Returns:
            str: A string that includes both the status code and the original error message.
        """
        return f"ColossusAPIError (Status Code: {self.status_code}): {super().__str__()}"
