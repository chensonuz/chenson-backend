from app.user.schemas import InitData, UserCreate


def auth_data_to_create_schema(request: InitData) -> UserCreate:
    return UserCreate(
        telegram_id=request.user.id,
        first_name=request.user.first_name,
        username=request.user.username,
    )
