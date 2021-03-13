import psycopg2
from Aashii.constants import Query


class Database:
    def __init__(self, database_url: str):

        """
        Initializes the PostgreSQL database connection.
        """

        self.connection = psycopg2.connect(database_url)

    def __del__(self):

        """
        Closes the connection automatically when
        the reference count drops to zero.
        """

        self.connection.close()

    def add_message(self, message_id: int, user_id: int):

        """
        Adds the user ID, message ID
        of the forwarded message to database.
        """

        cur = self.connection.cursor()
        cur.execute(
            Query.ADD_MESSAGE,
            {"message_id": message_id, "user_id": user_id},
        )
        self.connection.commit()
        cur.close()

    def add_user(self, user_id: int, username: str, full_name: str):

        """
        Adds the user with unblocked status.
        """

        cur = self.connection.cursor()
        cur.execute(
            Query.ADD_USER,
            {"user_id": user_id, "username": username, "full_name": full_name},
        )
        self.connection.commit()
        cur.close()

    def get_user_full_name(self, user_id: int):

        """
        Gets the full name of user based on the user ID.
        """

        cur = self.connection.cursor()
        cur.execute(Query.GET_USER_FULL_NAME, {"user_id": user_id})
        (full_name,) = next(cur, (None,))
        cur.close()
        return full_name

    def get_user_id(self, message_id: int):

        """
        Gets the user ID of the message ID forwarded by bot.
        """

        cur = self.connection.cursor()
        cur.execute(Query.GET_USER_ID, {"message_id": message_id})
        (user_id,) = next(cur, (None,))
        cur.close()
        return user_id

    def get_user_status(self, user_id: int):

        """
        Gets the user status as True if they
        are blocked and False on otherwise.
        """

        cur = self.connection.cursor()
        cur.execute(Query.GET_USER_STATUS, {"user_id": user_id})
        (status,) = next(cur, (False,))
        cur.close()
        return status

    def get_users(self):

        """
        Gets a list of all users in the database
        and the length of list.
        """

        cur = self.connection.cursor()
        cur.execute(Query.GET_USERS)
        users = [user_id for (user_id,) in cur]
        total = len(users)
        cur.close()
        return users, total

    def set_user_status(self, user_id: int, status: bool):

        """
        Sets the user status as True if they
        are blocked and False on otherwise.
        """

        cur = self.connection.cursor()
        cur.execute(Query.SET_USER_STATUS, {"user_id": user_id, "status": status})
        self.connection.commit()
        cur.close()
