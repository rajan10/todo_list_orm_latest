from sqlalchemy.orm import Session

from repository import UserRepository
from database import engine


def authenticate(username, password):
    with Session(engine) as session:
        user_repo = UserRepository(session=session)
        user = user_repo.get_by_username(username=username)

    return bool(user.password == password), user
