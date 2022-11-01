from user.repository import UserRepo
from provider.auth_provider import auth_provider


class UserService:
    def __init__(self) -> None:
        self.repo = UserRepo()

    def create(self, email: str, password: str, name: str) -> dict:
        password = auth_provider.hashpw(password)
        created_user = self.repo.create(
            name=name,
            email=email,
            password=password,
        )
        return created_user
