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

conn.commit()
conn.close()