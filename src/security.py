from fastapi import HTTPException, status
from fastapi.params import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer


def get_access_token(
        auth_header: HTTPAuthorizationCredentials | None
        = Depends(HTTPBearer(auto_error=False)),
) -> str:
    if auth_header is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, )
    return auth_header.credentials
