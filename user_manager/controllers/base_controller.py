from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from starlette import status
from starlette.responses import JSONResponse


class BaseController:
    @staticmethod
    def ise(exception: Exception):
        """Handle Internal Server Errors."""
        print(exception)
        if isinstance(exception, ValueError):
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exception))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='An error occurred, please contact the administration.'
        )

    @staticmethod
    def create_success(result=None, message="Created successfully."):
        """Handle successful creation responses."""
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                'status': 1,
                'message': message,
                'result': jsonable_encoder(result) if result else None
            }
        )

    @staticmethod
    def not_found(message="No records found."):
        """Handle not found responses."""
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                'status': 0,
                'message': message
            }
        )

    @staticmethod
    def success(result=None, message="Success."):
        """Handle general successful responses."""
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                'status': 1,
                'message': message,
                'result': jsonable_encoder(result) if result else None
            }
        )

    @staticmethod
    def bad_request(message="Invalid request."):
        """Handle bad request responses."""
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                'status': 0,
                'message': message
            }
        )

    @staticmethod
    def unauthorized_request(message="Unauthorized access."):
        """Handle unauthorized access responses."""
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={
                'status': 0,
                'message': message
            }
        )

    @staticmethod
    def custom_response(status_code: int, message: str, result=None):
        """Handle custom responses with a specified status code."""
        return JSONResponse(
            status_code=status_code,
            content={
                'status': 1 if status_code < 400 else 0,
                'message': message,
                'result': jsonable_encoder(result) if result else None
            }
        )
