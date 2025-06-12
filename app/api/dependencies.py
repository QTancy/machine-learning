# app/api/dependencies.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from app.core.config import settings


oauth2_scheme = HTTPBearer() 


async def get_current_user_id(token: HTTPAuthorizationCredentials  = Depends(oauth2_scheme)) -> int:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        jwt_token_string = token.credentials

        payload = jwt.decode(jwt_token_string, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_data = payload.get("user")
        if user_data is None or not isinstance(user_data, dict):
            raise credentials_exception
        user_id_from_payload = user_data.get("id")
        if user_id_from_payload is None:
            raise credentials_exception
        
        user_id: int = int(user_id_from_payload) 
    except (JWTError, ValueError): 
        raise credentials_exception
    return user_id