"""Authentication steps."""
import base64

from behave import given
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser

HTTP_HEADER_ENCODING = 'iso-8859-1'

User = get_user_model()


def basic_auth_header(username: str, password: str) -> str:
    """Return a dict with the basic auth header.

    Args:
        username (str): The username.
        password (str): The password.
    """
    credentials = f"{username}:{password}"
    base64_credentials = base64.b64encode(
        credentials.encode(HTTP_HEADER_ENCODING)
    ).decode(HTTP_HEADER_ENCODING)
    return f"Basic {base64_credentials}"


@given("I am a superuser")
def step_impl(context):
    """Setup superuser.

    Args:
        context (behave.runner.Context): The test context.
    """
    user = User.objects.create_user(
        username="test superuser",
        password="test",
        is_active=True,
        is_staff=True,
        is_superuser=True,
    )
    context.user = user
    context.test.client.force_login(user)


@given("I am a registered user")
def setup_registered_user(context):
    """Setup registered user.

    Args:
        context (behave.runner.Context): The test context.
    """
    user = User.objects.create_user(
        username="test user",
        password="test",
        is_active=True,
        is_staff=False,
        is_superuser=False,
    )
    context.user = user
    context.test.client.force_login(user)


@given("I am a staff user")
def setup_staff_user(context):
    """Setup staff user.

    Args:
        context (behave.runner.Context): The test context.
    """
    user = User.objects.create_user(
        username="test staff user",
        password="test",
        is_active=True,
        is_staff=True,
        is_superuser=False,
    )
    context.user = user
    context.test.client.force_login(user)


@given("I am an anonymous user")
def setup_anon_user(context):
    """Setup anonymous user.

    Args:
        context (behave.runner.Context): The test context.
    """
    context.user = AnonymousUser()
    context.credentials = basic_auth_header("test", "bad_password")
