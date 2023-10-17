import motor.motor_asyncio

from config import MONGO_DB_SERVER, MONGO_INITDB_ROOT_PASSWORD, MONGO_INITDB_ROOT_USERNAME

mongo_client = motor.motor_asyncio.AsyncIOMotorClient(
    f'mongodb://{MONGO_INITDB_ROOT_USERNAME}:{MONGO_INITDB_ROOT_PASSWORD}@{MONGO_DB_SERVER}:27017')
db = mongo_client.deep_links
