from core.models import PhoneUsers, PhoneUsersNumbers


def add_new_user(command):
    """ add new user to phone_book

    Args:
        command (dict):

    Returns:
        str: success or fail of operation
    """
    username = command["username"]
    phone_number = command["phone_number"]
    explanation = command["explanation"] if "explanation" in command else ''
    to_user = PhoneUsers.create(username=username, explanation=explanation)
    PhoneUsersNumbers.create(to_user=to_user, phone_number=phone_number)
    return f"phone user {username} added successfully"


def remove_user(command):
    """ remove user from phone_book

    Args:
        command (dict):

    Returns:
        str: success or fail of operation
    """
    username = command["username"]
    q = PhoneUsers.delete().where(PhoneUsers.username == username)
    q.execute()
    return f"phone user {username} removed successfully"


def edit_user(command):
    """edit a user

    Args:
        command (dict):

    Returns:
        str: success or fail of operation
    """
    username = command["username"]
    phone_number = command["phone_number"]
    new_username = command["new_username"]
    new_phone_number = command["new_phone_number"]
    user_info = PhoneUsers.get(PhoneUsers.username == username)
    if new_username is not None:
        q = PhoneUsers.update(username=new_username).where(PhoneUsers.username == username)
        q.execute()
    if new_phone_number is not None:
        q = PhoneUsersNumbers.update(phone_number=new_phone_number).where(PhoneUsersNumbers.to_user == user_info,
                                                                          PhoneUsersNumbers.phone_number == phone_number)
        q.execute()
    return f"information of user {username} updated successfully"


def get_all_users(command):
    """return all users info

    Args:
        command (dict):

    Returns:
        list of dict
    """
    all_users = []
    query = PhoneUsersNumbers.select().join(PhoneUsers)
    for q in query:
        all_usernames = [info["name"] for info in all_users]
        username = q.to_user.username
        if username in all_usernames:
            user_info = [info for info in all_users if info["name"] == username][0]
            user_info["phone_number"].append(q.phone_number)
        else:
            user_info = dict()
            user_info["name"] = username
            user_info["phone_number"] = [q.phone_number]
            user_info["explanation"] = q.to_user.explanation
            all_users.append(user_info)
    return all_users


def get_user_by_name(command):
    """return user info searched by name

    Args:
        command(dict):

    Returns:
        dict
    """
    username = command["username"]
    phone_numbers = []
    user_info = PhoneUsers.get(PhoneUsers.username == username)
    query = PhoneUsersNumbers.select().where(PhoneUsersNumbers.to_user == user_info)
    username = query.get().to_user.username
    for q in query:
        phone_numbers.append(q.phone_number)
    return {"name": username, "phone_numbers": phone_numbers}


def get_username_by_phone_number(command):
    """return user info searched by number

    Args:
        command(dict):

    Returns:
        dict
    """
    phone_number = command["phone_number"]
    phone_numbers = []
    query = PhoneUsersNumbers.select().join(PhoneUsers).where(PhoneUsersNumbers.phone_number == phone_number)
    username = query.get().to_user.username
    user_info = PhoneUsers.get(PhoneUsers.username == username)
    query = PhoneUsersNumbers.select().where(PhoneUsersNumbers.to_user == user_info)
    for q in query:
        phone_numbers.append(q.phone_number)

    return {"name": username, "phone_numbers": phone_numbers}


def add_phone_number(command):
    """add a new phone number to an existence user

    Args:
        command(dict):

    Returns:
        str: success or fail of operation
    """
    username = command["username"]
    phone_number = command["phone_number"]
    user_info = PhoneUsers.get(PhoneUsers.username == username)
    PhoneUsersNumbers.create(to_user=user_info, phone_number=phone_number)
    return f"new phone number {phone_number} registerd successfuly for user {username}"
