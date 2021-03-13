class Query:

    ADD_MESSAGE = "INSERT INTO messages VALUES (%(message_id)s, %(user_id)s) ;"

    ADD_USER = (
        "INSERT INTO users "
        "VALUES (%(user_id)s, %(username)s, %(full_name)s, FALSE) "
        "ON CONFLICT (user_id) DO UPDATE "
        "SET username = %(username)s, full_name = %(full_name)s;"
    )

    GET_USER_ID = "SELECT user_id FROM messages WHERE message_id = %(message_id)s;"

    GET_USER_FULL_NAME = "SELECT full_name FROM users WHERE user_id = %(user_id)s;"

    GET_USER_STATUS = "SELECT status FROM users WHERE user_id = %(user_id)s;"

    GET_USERS = "SELECT user_id FROM users;"

    SET_USER_STATUS = (
        "UPDATE users SET status = %(status)s WHERE user_id = %(user_id)s;"
    )
