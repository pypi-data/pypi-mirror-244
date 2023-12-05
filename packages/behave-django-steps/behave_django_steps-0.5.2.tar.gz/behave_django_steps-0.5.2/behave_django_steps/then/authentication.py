"""Steps for testing authentication."""
from behave import then


@then("I should be a superuser")
def is_superuser(context):
    """Check that a user is a superuser.

    Args:
        context (behave.runner.Context): The test context.
    """
    context.test.assertTrue(getattr(context, "user", None) is not None)
    context.test.assertTrue(context.user.is_superuser)


@then("I should not be a superuser")
def is_not_superuser(context):
    """Check that a user is not a superuser.

    Args:
        context (behave.runner.Context): The test context.
    """
    context.test.assertTrue(getattr(context, "user", None) is not None)
    context.test.assertFalse(context.user.is_superuser)


@then("I should be a staff user")
def is_staff_user(context):
    """Check that a user is a staff user.

    Args:
        context (behave.runner.Context): The test context.
    """
    context.test.assertTrue(getattr(context, "user", None) is not None)
    context.test.assertTrue(context.user.is_staff)


@then("I should not be a staff user")
def is_not_staff_user(context):
    """Check that a user is not a staff user.

    Args:
        context (behave.runner.Context): The test context.
    """
    context.test.assertTrue(getattr(context, "user", None) is not None)
    context.test.assertFalse(context.user.is_staff)
