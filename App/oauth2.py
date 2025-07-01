from fastapi import HTTPException
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi.security.oauth2 import OAuth2PasswordBearer
from . import schema
from fastapi import Depends, HTTPException, status
from App.config import setting

oauth2_schema = OAuth2PasswordBearer(tokenUrl='login')


SECRET_KEY = setting.secret_key
ALGORITHM = setting.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = setting.access_token_expire_minutes

def create_token(data : dict):
    """
        Create a JWT access token with an expiration time.

        Args:
            data: A dictionary containing user data to encode in the token.

        Returns:
            A JWT token as a string, signed with the secret key and containing an expiration claim.
        """
    to_encode = data.copy()


    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode,SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token : str, credentials_exceptions):
    """
        Decode and verify a JWT token.

        Args:
            token: The JWT token string to verify.
            credentials_exceptions: The HTTPException to raise if verification fails.

        Returns:
            tokenData: A schema instance containing the user's ID from the token.

        Raises:
            HTTPException: If the token is invalid or the user ID is missing.
        """
    try:
        payload = jwt.decode(token, SECRET_KEY, ALGORITHM)
        id: str = payload.get("user_ID")
        print(id)
        if not id:
            raise credentials_exceptions
        token_data = schema.tokenData(id=id)
    except JWTError as e:
        raise credentials_exceptions
    return token_data

def get_current_user(token : str = Depends(oauth2_schema)):
    """
        Extract the current authenticated user from the JWT token.

        Args:
            token: Automatically extracted from the Authorization header using the OAuth2 scheme.

        Returns:
            tokenData: The user information decoded from the JWT.

        Raises:
            HTTPException: If the token is missing or invalid.
        """
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="couldn't validate credentials" , headers={"WWW-Authenticate" :  "Bearer"})
    return verify_token(token,credentials_exception)



