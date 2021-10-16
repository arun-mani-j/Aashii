ALTER TABLE users RENAME status TO blocked;

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

INSERT INTO from_users (SELECT user_id, -1, message_id FROM messages);
DROP TABLE messages;
