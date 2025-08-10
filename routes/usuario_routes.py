from fastapi import APIRouter, HTTPException
from service.usuario_service import UsuarioService
from auth.auth_api import *

router = APIRouter(
    tags=["Usuário"]
)

usuario_service = UsuarioService()

@router.post("/registro", response_model=UserResponse)
def register_user(user: UserRequest):
    check_user = user_service.get_user_by_email(user.email)
    if check_user:
        raise HTTPException(status_code=400, detail="Email já registrado!")
    
    user_save = user_service.criar_usuario(user) 
    return UserResponse(id=user_save.id, nome=user_save.nome, email=user_save.email)


@router.post("/login", response_model=Token)
async def login(login_request: LoginRequest):
    """Autentica o usuário e retorna um token de acesso."""
    user = user_service.get_user_by_email(login_request.email) 
    if not user or not verify_password(login_request.password, user['password']):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Login ou Senha Inválidos!",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user['email']}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
