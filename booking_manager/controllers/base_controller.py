from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from starlette import status
from starlette.responses import JSONResponse


class BaseController:
    @staticmethod
    def ise(e: Exception):
        print(e)
        if type(e) is ValueError:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))

        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail='An error occurred, please contact the administration.!')

    @staticmethod
    def create_success(result):
        return {'status': 1, 'message': 'Added successfully.!', 'result': result}

    @staticmethod
    def not_found():
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                            content={'status': 0, 'message': 'No records found.!'})

    @staticmethod
    def success(result, message="success."):
        # Allow passing a custom success message
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content={'status': 1, 'message': message,
                                     'result': jsonable_encoder(result)})

    @staticmethod
    def bad_request(message: str = None):
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={'status': 0,
                                     'message': 'An error occurred, please contact the administration.!'})

    @staticmethod
    def unauthorized_request(message: str = None):
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={'status': 0, 'message': message})

    @staticmethod
    def _success(result):
        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(result))

