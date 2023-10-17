import uuid

from mongo_db import db


async def create_short_url(long_url, short_url=None, user_id=None):
    if short_url:
        link = await db.deep_links.find_one({"short_url": short_url})
        if link:
            return {"error": "short url already exists"}
    else:
        short_url = str(uuid.uuid4())
    data = {"short_url": short_url, "long_url": long_url}
    if user_id:
        data["user_id"] = user_id
    await db.deep_links.insert_one(data)
    return short_url


async def get_long_url(short_url: str):
    link = await db.deep_links.find_one({"short_url": short_url})
    if not link:
        return f"Long url for short url '{short_url}' does not exist. Use /create 'your long_url' command"
    return link["long_url"]


async def get_user_urls(user_id):
    links = db.deep_links.find({"user_id": user_id})
    data_as_list = await links.to_list(length=100)
    links_list = []
    for link in data_as_list:
        links_list.append(link)
    return links_list


async def get_user_redirects(user_id):
    redirects = db.redirects.aggregate([
        {"$match": {"owner": user_id}},
        {"$group": {"_id": "$short_url",
                    "count": {"$sum": 1}}}
    ])
    data_as_list = await redirects.to_list(length=100)
    redirects_list = []
    for link in data_as_list:
        redirects_list.append(link)
    return redirects_list
