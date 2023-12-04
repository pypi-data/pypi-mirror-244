import asyncio
from getpass import getpass
from uuid import UUID

from syndb_api.user.admin import create_user, delete_user_by_model, query_user


def _input_user_credentials(email: str | None, stdout_password: bool = False):
    print("Press enter when done with each input.")
    email = email or input("Email: ")

    if stdout_password:
        password = input("Password: ")
    else:
        while True:
            password = getpass()
            password_2 = getpass("Repeat password:")
            if password == password_2:
                break
            print("The two passwords do not match, try again")

    return email, password


def _create_user_query_coroutine(email: str | None = None, user_id: UUID | None = None):
    if email:
        return query_user(email=email)
    elif user_id:
        return query_user(user_id=user_id)
    else:
        return query_user(email=input("No credentials provided.\nEmail: "))


def cli_create_superuser(*_input_user_credentials_args, **_input_user_credentials_kwargs):
    print("YOU ARE CREATING A SUPERUSER!\n")
    email, password = _input_user_credentials(*_input_user_credentials_args, **_input_user_credentials_kwargs)
    return asyncio.run(create_user(email, password, is_superuser=True, is_verified=True))


def cli_create_verified_user(*_input_user_credentials_args, **_input_user_credentials_kwargs):
    print("YOU ARE CREATING A VERIFIED USER!\n")
    email, password = _input_user_credentials(*_input_user_credentials_args, **_input_user_credentials_kwargs)
    return asyncio.run(create_user(email, password, is_superuser=False, is_verified=True))


def cli_delete_user(new_owner: UUID | None = None, **user_query_kwargs):
    user = asyncio.run(_create_user_query_coroutine(**user_query_kwargs))
    if (
        input(
            f"\nid: {user.id}\nemail: {user.email}\njoined on: {user.join_timestamp}\n\n"
            f"Are you sure that you want to delete the following user? (y/N) "
        ).lower()
        == "y"
    ):
        if user.has_uploaded:
            if new_owner is None:
                return print("New owner of data must be designated before deletion, define UUID in the new_owner kwarg")
            # TODO: Add ownership transfer function
        asyncio.run(delete_user_by_model(user))
    else:
        print("Aborted operation by CLI client")


def cli_flip_superuser(**user_query_kwargs):
    user = asyncio.run(_create_user_query_coroutine(**user_query_kwargs))
    if input(f"{user.id} superuser state is set to {user.is_superuser}, proceed with flip? y/N: ").lower() != "y":
        return print("Aborted operation by CLI client")
    user.is_superuser = not user.is_superuser
    user.save(update_fields=["is_superuser"])
    print(f"{user.id} superuser state is set to {user.is_superuser}; it was {not user.is_superuser}")
