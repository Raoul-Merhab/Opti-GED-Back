from os import getenv
from dotenv import load_dotenv

load_dotenv()

DatabaseCreds = {
    "User": getenv("DB_USER"),
    "Password": getenv("DB_PASSWORD"),
    "Host": getenv("DB_HOST"),
    "Name": getenv("DB_NAME"),
    "Port": getenv("DB_PORT"),
    "Link":f'mysql+pymysql://{getenv("DB_USER")}:{getenv("DB_PASSWORD")}@{getenv("DB_HOST")}:{getenv("DB_PORT")}/{getenv("DB_NAME")}'
}