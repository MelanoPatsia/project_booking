import sqlite3

conn = sqlite3.connect("project_booking.db")

c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS projects (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    title TEXT NOT NULL,

    short_description TEXT NOT NULL,

    full_description TEXT NOT NULL,

    image_link TEXT NOT NULL,

    project_status TEXT NOT NULL

)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS users (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    name TEXT NOT NULL,

    email TEXT NOT NULL,

    password TEXT NOT NULL

)
""")

#c.execute("""
#INSERT INTO users (name, email, password)
#VALUES (?, ?, ?)
#""", (
#    "Melano",
#    "admin@gzaari.ge",
#    "admin_password_2026"
#))

conn.commit()
conn.close()