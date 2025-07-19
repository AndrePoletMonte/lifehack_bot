CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    language TEXT DEFAULT 'English'
);

CREATE TABLE IF NOT EXISTS lifehacks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text TEXT NOT NULL,
    language TEXT NOT NULL
);

INSERT INTO lifehacks (text, language) VALUES
('Drink water first thing in the morning.', 'English'),
('Set a timer to stay focused for 25 minutes (Pomodoro).', 'English'),
('Pij vodu odmah nakon buđenja.', 'Serbian'),
('Koristi tajmer od 25 minuta za fokus (Pomodoro metoda).', 'Serbian');
