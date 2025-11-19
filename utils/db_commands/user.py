from core.database_settings import database
from core.models import users


async def add_user(data: dict) -> dict | None:
    try:
        query = users.insert().values(
            full_name=data.get("full_name"),
            phone_number=data.get("phone_number"),
            chat_id=data.get("chat_id"),
            age=int(data.get("age")),
            language=data.get("language"),
            created_at=data.get("created_at"),
            updated_at=data.get("created_at")
        )
        new_user = await database.execute(query=query)
        return new_user
    except Exception as e:
        error_text = f"Error appeared when getting user: {e}"
        print(error_text)
        return None
