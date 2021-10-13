"""Contains the Query object."""


class Query:
    """Query object contains constant query strings used\
    by the database to get and set values."""

    ADD_ADMIN_MESSAGE = (
        "INSERT INTO from_admins "
        "VALUES (%(message_id)s, %(user_id)s, %(dest_message_id)s);"
    )

    ADD_USER_MESSAGE = (
        "INSERT INTO from_users "
        "VALUES (%(user_id)s, %(message_id)s, %(dest_message_id)s);"
    )

    ADD_USER = (
        "INSERT INTO users "
        "VALUES (%(user_id)s, %(username)s, %(full_name)s, FALSE) "
        "ON CONFLICT (user_id) DO UPDATE "
        "SET username = %(username)s, full_name = %(full_name)s;"
    )

    GET_DEST_MESSAGE_ID_USERS = (
        "SELECT dest_message_id FROM from_users "
        "WHERE user_id = %(user_id)s AND message_id = %(message_id)s;"
    )

    GET_MESSAGE_ID_ADMINS = (
        "SELECT message_id FROM from_admins "
        "WHERE user_id = %(user_id)s AND dest_message_id = %(dest_message_id)s;"
    )

    GET_USER = (
        "SELECT username, full_name, blocked FROM users WHERE user_id = %(user_id)s;"
    )

    GET_USER_DEST_MESSAGE_ID_ADMINS = (
        "SELECT user_id, dest_message_id FROM from_admins "
        "WHERE message_id = %(message_id)s;"
    )

    GET_USER_FULL_NAME = "SELECT full_name FROM users WHERE user_id = %(user_id)s;"

    GET_USER_MESSAGE_ID_USERS = (
        "SELECT user_id, message_id FROM from_users "
        "WHERE dest_message_id = %(dest_message_id)s;"
    )

    GET_USER_BLOCKED = "SELECT blocked FROM users WHERE user_id = %(user_id)s;"

    GET_USERS = "SELECT user_id FROM users;"

    SET_USER_BLOCKED = (
        "UPDATE users SET blocked = %(blocked)s WHERE user_id = %(user_id)s;"
    )
