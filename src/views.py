from sqlalchemy.orm import Session

from repository import UserRepository
from database import engine
from custom_exception import NoObjectInDatabase, AuthenticationFailed
import logging

logger = logging.getLogger()


def authenticate(username, password):
    with Session(engine) as session:
        user_repo = UserRepository(session=session)
        try:
            user = user_repo.get_by_username(username=username)
        except NoObjectInDatabase as exc:
            raise AuthenticationFailed("Authentication Failed ") from exc

    return bool(user.password == password), user
