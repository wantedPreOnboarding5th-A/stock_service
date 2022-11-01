from user.models import User
from user.serializers import UserSerializer
from exceptions import NotFoundError


class UserRepo:
    def __init__(self) -> None:
        self.model = User
        self.serializer = UserSerializer

    def get(self, user_id: int) -> dict:
        try:
            return UserSerializer(self.model.objects.get(id=user_id)).data
        except self.model.DoesNotExist:
            raise NotFoundError

    def get_by_email(self, email: str):
        try:
            return UserSerializer(self.model.objects.get(email=email)).data
        except self.model.DoesNotExist:
            raise NotFoundError

    def get_by_account_number(self, account_number: int):
        """ 계좌번호로 유저 정보를 찾는 메서드 """
        try:
            return UserSerializer(
                self.model.objects.prefetch_related("Account").filter(
                    account__number__exact=account_number
                ).get()
            )
        except self.model.DoesNotExist:
            raise NotFoundError

    def create(self, name: str, email: str, password: str):
        serializer = self.serializer(
            data={
                "name": name,
                "email": email,
                "password": password,
            }
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.data
