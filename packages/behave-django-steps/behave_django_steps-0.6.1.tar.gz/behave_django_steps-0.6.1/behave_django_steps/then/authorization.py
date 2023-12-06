"""Steps for testing authorization."""
from behave import then


@then('I should have the role "{role_name}"')
def has_role(context, role_name):
    """Check that the user has the role.

    Args:
        context (behave.runner.Context): The test context.
        role_name (str): The name of the role.
    """
    context.test.assertTrue(getattr(context, "user", None) is not None)
    context.test.assertTrue(context.user.groups.filter(name=role_name).exists())


@then('I should have the group "{group_name}"')
def has_group(context, group_name):
    """Check that the user has the group.

    Args:
        context (behave.runner.Context): The test context.
        group_name (str): The name of the group.
    """
    context.execute_steps(f'Then I should have the role "{group_name}"')


@then('I should not have the role "{role_name}"')
def does_not_have_role(context, role_name):
    """Check that the user does not have the role.

    Args:
        context (behave.runner.Context): The test context.
        role_name (str): The name of the role.
    """
    context.test.assertTrue(getattr(context, "user", None) is not None)
    context.test.assertFalse(context.user.groups.filter(name=role_name).exists())


@then('I should not have the group "{group_name}"')
def does_not_have_group(context, group_name):
    """Check that the user does not have the group.

    Args:
        context (behave.runner.Context): The test context.
        group_name (str): The name of the group.
    """
    context.execute_steps(f'Then I should not have the role "{group_name}"')


@then('I should have the permission "{permission_name}" for model "{model_name}"')
def has_permission(context, permission_name, model_name):
    """Check that the user has the role.

    Args:
        context (behave.runner.Context): The test context.
        permission_name (str): The name of the role.
        model_name (str): The name of the model.
    """
    context.test.assertTrue(getattr(context, "user", None) is not None)
    context.execute_steps(f'Given a "{model_name}" model is available')
    app_label = context.models[  # pylint: disable=protected-access
        model_name
    ]._meta.app_label
    context.test.assertTrue(context.user.has_perm(f"{app_label}.{permission_name}"))


@then('I should not have the permission "{permission_name}" for model "{model_name}"')
def does_not_have_permission(context, permission_name, model_name):
    """Check that the user does not have the role.

    Args:
        context (behave.runner.Context): The test context.
        permission_name (str): The name of the role.
        model_name (str): The name of the model.
    """
    context.test.assertTrue(getattr(context, "user", None) is not None)
    context.execute_steps(f'Given a "{model_name}" model is available')
    app_label = context.models[  # pylint: disable=protected-access
        model_name
    ]._meta.app_label
    context.test.assertFalse(context.user.has_perm(f"{app_label}.{permission_name}"))
