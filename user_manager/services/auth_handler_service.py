import jwt
from datetime import datetime, timedelta
from typing import Optional
from passlib.context import CryptContext
import configparser
import os


class AuthHandlerService:
    def __init__(self):
        # Load the configuration and retrieve the secret key
        config = configparser.ConfigParser()
        config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), '.cfg')
        config.read(config_path)

        # Secret key and hashing algorithm
        self.secret_key = config['JWT'].get('SECRET_KEY')
        self.algorithm = config['JWT'].get('ALGORITHM')

        # Password hashing setup
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def encode_token(self, user_id: str) -> str:
        expiration = datetime.utcnow() + timedelta(hours=1)
        payload = {
            "sub": user_id,
            "exp": expiration
        }
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    def decode_token(self, token: str) -> Optional[dict]:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

    def hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)
