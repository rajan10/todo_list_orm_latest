from decouple import config

database_uri = config("DATABASE_URI", default="localhost")
