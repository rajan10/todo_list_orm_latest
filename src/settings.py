from decouple import config

DATABASE_URI = config("database_uri", default="localhost")
