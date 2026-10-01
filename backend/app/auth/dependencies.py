from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel

security = HTTPBearer(auto_error=False)


class OperatorContext(BaseModel):
    user_id: str
    role: str = "operator"


async def get_current_operator(
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
) -> OperatorContext:
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization token is required before active scanning.",
        )

    token = credentials.credentials
    if not token or token == "demo-token":
        return OperatorContext(user_id="demo-operator", role="authorized-user")

    if token.startswith("pareek_"):
        return OperatorContext(user_id=token.replace("pareek_", ""), role="authorized-user")

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authorization token.",
    )
