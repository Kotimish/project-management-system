from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from monolith.auth.application.dtos.user import CreateUserCommand, LoginUserCommand
from monolith.auth.application.exceptions import auth_exceptions as exceptions
from monolith.auth.application.interfaces.services.auth_service import IAuthenticationService
from monolith.auth.application.interfaces.services.token_service import ITokenService
from monolith.auth.application.interfaces.services.user_service import IUserService
from monolith.auth.presentation.api.dependencies import get_user_service, get_auth_service, get_token_service
from monolith.auth.presentation.schemas.login import LoginRequest, LoginResponse
from monolith.auth.presentation.schemas.logout import LogoutResponseScheme
from monolith.auth.presentation.schemas.token import TokenResponse, DecodeTokenResponse
from monolith.auth.presentation.schemas.user import RegistrateUserRequest, RegistrateUserResponse

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


@router.post("/register", response_model=RegistrateUserResponse)
async def register(
        request: RegistrateUserRequest,
        service: IUserService = Depends(get_user_service)
):
    """Регистрация нового пользователя."""
    user = CreateUserCommand(
        login=request.login,
        email=request.email,
        password=request.password
    )
    try:
        response = await service.create_user(user)
    except exceptions.InvalidRoleException:
        raise HTTPException(status_code=500, detail="Default role not found")
    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error")
    return RegistrateUserResponse(id=response.id)


@router.post("/login")
async def login(
        request: LoginRequest,
        service: IAuthenticationService = Depends(get_auth_service)
):
    """Аутентификация пользователя, создание сессии, выдача токенов."""
    session = LoginUserCommand(
        login=request.login,
        password=request.password
    )
    try:
        response = await service.login_user(session)
    except exceptions.InvalidLoginException:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    except exceptions.InvalidPasswordException:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    except exceptions.InactiveUserException:
        raise HTTPException(status_code=403, detail="User account is inactive")
    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error")
    return LoginResponse(
        access_token=response.access_token,
        refresh_token=response.refresh_token
    )


@router.post("/logout", response_model=LogoutResponseScheme)
async def logout(
        refresh_token: Annotated[str, Depends(oauth2_scheme)],
        service: IAuthenticationService = Depends(get_auth_service)
):
    """Выход пользователя, отзыв токенов, удаление сессии."""
    try:
        await service.logout_user(refresh_token)
    except exceptions.InvalidSessionException:
        raise HTTPException(status_code=401, detail="Session invalid or already revoked")
    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error")
    return LogoutResponseScheme(msg="Successfully logout")


@router.post("/refresh", response_model=TokenResponse)
async def refresh(
        refresh_token: Annotated[str, Depends(oauth2_scheme)],
        service: IAuthenticationService = Depends(get_auth_service)
):
    """Обновление короткоживущего токена (access_token) с использованием долгоживущего токена (refresh_token)."""
    try:
        access_token = await service.refresh_access_token(refresh_token)
    except exceptions.InvalidSessionException:
        raise HTTPException(status_code=401, detail="Session not found")
    except exceptions.InactiveSessionException:
        raise HTTPException(status_code=401, detail="Inactive session")
    except exceptions.NotFoundUserException:
        raise HTTPException(status_code=500, detail="User not found")
    except exceptions.InactiveUserException:
        raise HTTPException(status_code=401, detail="Inactive user")
    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error")
    return TokenResponse(token=access_token)


@router.post("/verify", response_model=DecodeTokenResponse)
async def verify_token(
        access_token: Annotated[str, Depends(oauth2_scheme)],
        service: ITokenService = Depends(get_token_service)
):
    """Проверка короткоживущего токена (access_token) для других сервисов, возврат информации из токена."""
    payload = service.decode_token(access_token)
    return DecodeTokenResponse(**payload)
