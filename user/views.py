from django.http import JsonResponse
from provider.auth_provider import AuthProvider
from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser
from drf_yasg.utils import swagger_auto_schema
from decorators.execption_handler import execption_hanlder
from user.service import UserService
from user.serializers import UserSignUpSchema, UserSignupSerializer

user_service = UserService()
auth_provider = AuthProvider()


@api_view(["POST"])
@execption_hanlder()
@parser_classes([JSONParser])
@swagger_auto_schema(
    responses={"access": "encoded_jwt"},
)
def login(request):
    email = request.data["email"]
    password = request.data["password"]
    auth_token = auth_provider.login(email, password)
    return JsonResponse(auth_token, status=status.HTTP_201_CREATED)


@api_view(["POST"])
@execption_hanlder()
@parser_classes([JSONParser])
@swagger_auto_schema(
    request_body=UserSignUpSchema,
    responses={201: UserSignupSerializer},
)
def signup(request):
    params = request.data
    params = UserSignUpSchema(data=params)
    params.is_valid(raise_exception=True)
    created_user = user_service.create(**params.data)
    return JsonResponse(created_user, status=status.HTTP_201_CREATED)


@api_view(["POST"])
@execption_hanlder()
@parser_classes([JSONParser])
@swagger_auto_schema(
    responses={"access": "encoded_jwt"},
)
def signout(request):
    auth_token = request.META.get("HTTP_AUTHORIZATION", None)
    if auth_token != None:
        auth_token = auth_provider.logout(auth_token)
    return JsonResponse(auth_token, status=status.HTTP_200_OK)
