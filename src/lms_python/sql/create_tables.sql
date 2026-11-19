CREATE TABLE IF NOT EXISTS rooms (
    id INTEGER PRIMARY KEY,
    room_name VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY,
    full_name VARCHAR(150) NOT NULL,
    birthday TIMESTAMP NOT NULL CHECK (birthday <= CURRENT_TIMESTAMP),
    gender CHAR(1) NOT NULL CHECK (gender IN ('M', 'F')),
    room_id INT NOT NULL,
    CONSTRAINT fk_students_room
        FOREIGN KEY (room_id)
        REFERENCES rooms(id)
        ON DELETE CASCADE
);
