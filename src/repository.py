from sqlalchemy import select
from sqlalchemy.orm import Session
from models import User, Task
from custom_exception import NoUserInDatabase


class UserRepository:
    def __init__(
        self,
        session: Session,
    ) -> None:
        self.session = session

    def get_all(
        self,
    ) -> list[User]:
        stmt = select(User)
        return self.session.scalars(stmt).all()

    def get_by_id(
        self,
        id: int,
    ) -> User:
        stmt = select(User).where(User.id == id)
        return self.session.scalar(stmt)

    def get_by_username(
        self,
        username: str,
    ) -> User:
        stmt = select(User).where(User.username == username)
        user = self.session.scalar(stmt)
        if not user:
            raise NoUserInDatabase("No such username in the database")

    def create_user(
        self,
        username: str,
        password: str,
    ) -> User:
        user = User(
            username=username,
            password=password,
        )
        self.session.add(user)
        self.session.commit()
        return user


class TaskRepository:
    def __init__(self, user: User, session: Session) -> None:
        self.session = session
        self.user = user

    def get_all(
        self,
    ) -> list[Task]:
        stmt = select(Task).where(Task.user == self.user)
        return self.session.scalars(stmt).all()

    def get_by_id(self, id: int) -> Task:
        stmt = select(Task).where(Task.user == self.user).where(Task.id == id)
        return self.session.scalar(stmt)

    def create_task(self, name: str, status: bool = False) -> Task:
        task = Task(
            name=name,
            status=status,
            user_id=self.user.id,
        )
        self.session.add(task)
        self.session.commit()
        return task

    def update_task(self, id: int, name: str, status: bool):
        task = self.get_by_id(id=id)
        task.name = name
        task.status = status
        self.session.commit()

    def delete_task_by_id(self, id: int) -> None:
        task = self.get_by_id(id=id)
        if task:
            self.session.delete(task)
            self.session.commit()
