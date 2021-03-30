CREATE TABLE IF NOT EXISTS users (
       user_id BIGINT PRIMARY KEY,
       username TEXT,
       full_name TEXT,
       status BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS messages (
       message_id INTEGER PRIMARY KEY,
       user_id BIGINT REFERENCES users ON DELETE CASCADE
);
