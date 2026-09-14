from peewee import *

db = SqliteDatabase('sab.db', timeout=70, pragmas=(('foreign_keys', 'on'),))


class Users(Model):
    username = CharField(unique=True, null=False, default='')
    email = CharField(null=True)
    password = CharField(null=False, default='')
    salt = CharField(unique=True, null=False, default='')

    class Meta:
        global db
        database = db
        db_table = 'user_table'


class PhoneUsers(Model):
    username = CharField(unique=True, null=False, default='')
    explanation = CharField(null=True)

    class Meta:
        global db
        database = db
        db_table = 'phone_user_table'


class PhoneUsersNumbers(Model):
    phone_number = CharField(unique=True, null=False, default='')
    to_user = ForeignKeyField(model=PhoneUsers, related_name='numbers', on_delete='CASCADE')

    class Meta:
        global db
        database = db
        db_table = 'phone_number_table'


def before_request(atomic_transaction=False):
    """ This function makes a connection to the database.
        Also, if tables was not created then it calls create_database_tables()
        and it creates database tables.
    Args:
        atomic_transaction (bool): if it was True then body of this function to be ignored.
    """
    if not atomic_transaction:
        create_database_tables()
        db.connect()


def teardown_request(atomic_transaction=False):
    """ This function close opened database connection
    Args:
        atomic_transaction (bool): if it was True then body of this function to be ignored.
    """
    if not atomic_transaction:
        db.close()


def create_database_tables():
    """ This function creates the tables of the database.
        If tables exist, it does nothing.

    Returns:

    """

    global db
    if db.is_closed():
        db.connect()

    tables = get_all_tables()
    db.create_tables(tables, safe=True)
    db.close()


def get_all_tables():
    return [Users, PhoneUsers, PhoneUsersNumbers]
