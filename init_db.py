import os
import psycopg2
import settings

conn = psycopg2.connect(
    host="localhost",
    database="who-just-unfollowed-me",
    user=settings.DB_USERNAME,
    password=settings.DB_PASSWORD
)

cur = conn.cursor()
