from environment import get_environment

MONGO_DB_SERVER = get_environment("MONGO_DB_SERVER")
MONGO_INITDB_ROOT_USERNAME = get_environment("MONGO_INITDB_ROOT_USERNAME")
MONGO_INITDB_ROOT_PASSWORD = get_environment("MONGO_INITDB_ROOT_PASSWORD")
TELEBOT_TOKEN = get_environment("TELEBOT_TOKEN")
