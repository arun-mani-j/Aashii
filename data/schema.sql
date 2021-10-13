CREATE TABLE users (
    user_id BIGINT PRIMARY KEY,
    username TEXT,
    full_name TEXT NOT NULL,
    blocked BOOL DEFAULT FALSE
);

CREATE TABLE from_admins (
    message_id INTEGER NOT NULL,
    user_id BIGINT REFERENCES users,
    dest_message_id INTEGER NOT NULL
);

CREATE TABLE from_users (
    user_id BIGINT REFERENCES users,
    message_id INTEGER NOT NULL,
    dest_message_id INTEGER NOT NULL
);
