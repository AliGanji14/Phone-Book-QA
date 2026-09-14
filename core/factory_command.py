from core.auth import sign_up, sign_in, logout
from core.phone_book import add_new_user, remove_user, edit_user, get_all_users, get_user_by_name, \
    get_username_by_phone_number, add_phone_number

function_mappings = {
    'sign_up': sign_up,
    'sign_in': sign_in,
    'logout': logout,
    'add_phone_user': add_new_user,
    'remove_phone_user': remove_user,
    'edit_phone_user': edit_user,
    'get_all_phone_users': get_all_users,
    'get_phone_user_by_name': get_user_by_name,
    'get_phone_user_by_number': get_username_by_phone_number,
    'add_phone_number': add_phone_number,
}


def call_func(command):
    return function_mappings[command["command_name"]](command["parameters"])
