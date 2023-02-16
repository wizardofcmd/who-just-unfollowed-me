import os
import psycopg2
import settings

conn = psycopg2.connect(
    host="localhost",
    database="local_db",
    user=settings.DB_USERNAME,
    password=settings.DB_PASSWORD
)

cur = conn.cursor()
cur.execute('DROP TABLE IF EXISTS books;')
cur.execute('CREATE TABLE users (id serial PRIMARY KEY,'
                                 'username varchar (50) NOT NULL,'
                                 'email varchar (100) NOT NULL,'
                                 'profile_pic varchar (150) NOT NULL);'
                                 )
conn.commit()

cur.close()
conn.close()
