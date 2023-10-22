from app.user.schemas.telegram import InitData
from app.user.schemas.user import UserCreate


def auth_data_to_create_schema(request: InitData) -> UserCreate:
    return UserCreate(
        telegram_id=request.user.id,
        first_name=request.user.first_name,
        username=request.user.username,
    )
