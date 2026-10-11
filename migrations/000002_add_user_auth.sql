CREATE TABLE IF NOT EXISTS user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    display_name TEXT NOT NULL,
    created_at TEXT
);

-- Add user ownership to wardrobe items.
-- Default 1 so the existing seed data belongs to the first registered user.
ALTER TABLE wardrobe_item ADD COLUMN user_id INTEGER DEFAULT 1;
