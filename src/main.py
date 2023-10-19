from sqlalchemy.orm import Session
from repository import UserRepository, TaskRepository
from database import engine
from views import authenticate
from sqlalchemy.exc import OperationalError
from traceback import print_exc
import logging
from utils import requires_numeric_option
from custom_exception import AuthenticationFailed, HomePageException, NoObjectInDatabase

logger = logging.getLogger()


class Prompt:
    @requires_numeric_option
    def home(self) -> int:
        print("\nWelcome to Todo List\n")
        option = input(
            "Enter the number to select. \n 1. Register \n 2. Login \n 3. Exit \n Enter the number:"
        )
        return option

    def creds(self):
        username = input("Enter username: ")
        password = input("Enter password: ")
        return username, password

    def task_input(self):
        name = input("Enter task name: ")
        return name

    @requires_numeric_option
    def todo_interface(self):
        option = input(
            """Enter the number to select.\n
               1. Create Task
               2. Read all Task
               3. Update Task
               4. Delete Task
               5. Exit
            """
        )

        return option

    def updated_successfully(self) -> None:
        print("Updated Succesfully!")

    def display_user(self, user):
        print(f"User Id: {user.id} \nUsername: {user.username}")

    def display_task(self, task):
        if isinstance(task, list):  # checking whether task is type list or not
            for member in task:
                print(
                    f"Task Id: {member.id} \nTask name {member.name} \n Task status {member.status}"
                )
            return
        print(
            f"Task Id: {task.id} \nTask name {task.name} \n Task status {task.status}"
        )

    def login_failed(self):
        print("Login failed, Incorrect creds")

    def end(self):
        print("Thank you for using Todo Application.")

    def input_task_id(self) -> int:
        task_id = int(input(" Input task id:"))
        return task_id

    def update_task_input(self):
        task_name = input("Enter the task name to update:")
        task_status = eval(input("Is it complete? (True/False)"))
        return task_name, task_status

    def invalid_input(self):
        print("Invalid input. \n Please enter the number from option menu.")


class Todo:
    def __init__(self, session: Session) -> None:
        self.session = session
        self.logged_user = None
        self.user_repo = UserRepository(session=session)
        self.prompt = Prompt()

    def home_page(self):
        while True:
            try:
                option = self.prompt.home()
                if option == 1:
                    username, password = self.prompt.creds()
                    user = self.user_repo.create_user(
                        username=username, password=password
                    )
                    return user
                if option == 2:
                    username, password = self.prompt.creds()
                    flag, user = authenticate(username=username, password=password)
                    if not flag:
                        self.prompt.login_failed()
                        self.prompt.end()
                        continue
                    return user
                if option == 3:
                    self.prompt.end()
                else:
                    self.prompt.invalid_input()
                    logger.info("invalid input, input value: %s", str(option))

            except ValueError as exc:
                self.prompt.invalid_input()
                logger.info("Invalid input, Input Value: %s", str(exc))

            except AuthenticationFailed as exc:
                raise HomePageException("Error in Home Page") from exc

    def todo_interface(self, user):
        task_repo = TaskRepository(user=user, session=self.session)
        while True:
            try:
                option = self.prompt.todo_interface()
                if option == 1:
                    task_name = self.prompt.task_input()
                    task = task_repo.create_task(name=task_name)
                    self.prompt.display_task(task=task)

                if option == 2:
                    tasks = task_repo.get_all()
                    self.prompt.display_task(task=tasks)

                if option == 3:
                    tasks = task_repo.get_all()
                    self.prompt.display_task(task=tasks)
                    task_id = self.prompt.input_task_id()
                    task_name, task_status = self.prompt.update_task_input()
                    task_repo.update_task(
                        id=task_id, name=task_name, status=task_status
                    )
                    self.prompt.updated_successfully()

                if option == 4:
                    tasks = task_repo.get_all()
                    self.prompt.display_task(task=tasks)
                    task_id = self.prompt.input_task_id()
                    task_repo.delete_task_by_id(id=task_id)

                if option == 5:
                    self.prompt.end()
                    break
            except NoObjectInDatabase as exc:
                print(str(exc))
                logger.error(str(exc))
            except Exception as exc:
                print("An error occured", str(exc))


def main():
    try:
        with Session(
            engine
        ) as session:  #  session obj is created using the 'engine'.In SQLALchemy, a session is a way to
            # interact with db
            todo = Todo(session=session)
            user = todo.home_page()
            todo.todo_interface(user=user)
    except OperationalError as exc:
        logger.exception(f"Databse error occured, {exc}")

    except HomePageException as exc:
        logger.exception(f"Home page error: {exc}")
    except Exception:
        print("Error occured...")
        print_exc()

    finally:
        print("\033[92m Code written by rajan\033[00m")


if __name__ == "__main__":
    main()
