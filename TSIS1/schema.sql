-- 1. Топтар кестесі
CREATE TABLE IF NOT EXISTS groups (
    id   SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

-- 2. Контактілер кестесі
CREATE TABLE IF NOT EXISTS contacts (
    id         SERIAL PRIMARY KEY,
    name       VARCHAR(100) NOT NULL,
    email      VARCHAR(100),
    birthday   DATE,
    group_id   INTEGER REFERENCES groups(id) ON DELETE SET NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. Телефондар кестесі (Бір контактіде бірнеше телефон болуы үшін)
CREATE TABLE IF NOT EXISTS phones (
    id         SERIAL PRIMARY KEY,
    contact_id INTEGER REFERENCES contacts(id) ON DELETE CASCADE,
    phone      VARCHAR(20) NOT NULL,
    type       VARCHAR(10) CHECK (type IN ('home', 'work', 'mobile'))
);

-- Стандартты топтарды бірден қосу
INSERT INTO groups (name) VALUES ('Family'), ('Work'), ('Friend'), ('Other') 
ON CONFLICT (name) DO NOTHING;