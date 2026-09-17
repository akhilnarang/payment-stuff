from fastapi import status
from starlette.exceptions import HTTPException


class NotFoundException(HTTPException):
    def __init__(self, detail: str = "Not Found") -> None:
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class BadRequestException(HTTPException):
    def __init__(self, detail: str = "Bad Request") -> None:
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)
