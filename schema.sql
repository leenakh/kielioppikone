CREATE TABLE users (id SERIAL PRIMARY KEY, first_name text, last_name TEXT, username TEXT UNIQUE, password TEXT, role TEXT);
CREATE TABLE words (id SERIAL PRIMARY KEY, lemma TEXT UNIQUE);
CREATE TABLE definitions (id SERIAL PRIMARY KEY, definition TEXT UNIQUE);
CREATE TABLE courses (id SERIAL PRIMARY KEY, teacher_id INTEGER REFERENCES users, subject TEXT UNIQUE);
CREATE TABLE questions (id SERIAL PRIMARY KEY, course_id INTEGER REFERENCES courses, word_id INTEGER REFERENCES words, definition_id INTEGER REFERENCES definitions, inflection TEXT);
CREATE TABLE answers (id SERIAL PRIMARY KEY, user_id INTEGER REFERENCES users, question_id INTEGER REFERENCES questions, course_id INTEGER REFERENCES courses, answered TIMESTAMP, correct BOOLEAN);
CREATE TABLE enrollments (id SERIAL PRIMARY KEY, user_id INTEGER UNIQUE REFERENCES users, course_id INTEGER REFERENCES courses, entered TIMESTAMP)
