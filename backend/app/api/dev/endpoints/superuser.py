from app.core.container import Container
from app.core.middleware import inject
from app.schema.auth_schema import SignUp
from app.schema.user_schema import User
from app.services.auth_service import AuthService
from dependency_injector.wiring import Provide
from fastapi import APIRouter, Depends

router = APIRouter(prefix="/superuser", tags=["dev"])


@router.post("", response_model=User)
@inject
def create_superuser(
    user_info: SignUp,
    service: AuthService = Depends(Provide[Container.auth_service]),
):
    """Create a new superuser (development only)."""
    return service.create_super_user(user_info)
