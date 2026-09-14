import bcrypt as bcrypt
import peewee

from core.models import before_request, Users, teardown_request


def sign_up(command):
    """register new auth user

    Args:
        command(dict):

    Returns:
        str
    """
    before_request()  # connect to database
    password = command["password"]
    email = command["email"]
    username = command["username"]
    # hash user password
    salt = bcrypt.gensalt(rounds=5)
    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), salt)

    # add a new user row to the user table
    Users.create(username=username, email=email, password=hashed_pw, salt=salt)
    teardown_request()  # close database connection
    return f"user {username} added successfully"


def sign_in(command):
    """login user

    Args:
        command(dict):

    Returns:

    """
    from server import online_users

    username = command["username"]
    password = command["password"]
    try:
        before_request()  # connect to database
        user = Users.get(Users.username == username)
        teardown_request()  # close database connection

        if bcrypt.hashpw(password.encode('utf-8'), bytes(user.salt, 'utf-8')) == bytes(user.password, "utf-8"):
            online_users.append(username)
        else:
            raise Exception("password is wrong")
    except peewee.DoesNotExist:
        message = 'User %s does not exist' % username, 'check_password'
        raise Exception(message)
    finally:
        teardown_request()  # close database connection
    return f"user {username} signed in successfully"


def logout(command):
    """logout user

    Args:
        command(dict):

    Returns:

    """
    from server import online_users
    username = command["username"]
    if username in online_users:
        online_users.remove(username)
    return f"user {username} signed out successfully"
