import uuid
from typing import Annotated, Optional

import motor.motor_asyncio
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, RedirectResponse

app = FastAPI()
mongo_client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://root:example@mongo_db:27017')
db = mongo_client.deep_links


@app.post("/")
async def root(long_url: Annotated[str, Form()], short_url: Optional[str] = Form(None)):
    if short_url:
        link = await db.deep_links.find_one({"short_url": short_url})
        if link:
            return {"error": "short url already exists"}
    else:
        short_url = str(uuid.uuid4())
    await db.deep_links.insert_one({"short_url": short_url, "long_url": long_url})
    return short_url


@app.get("/{short_url}")
async def to_long(short_url: str):
    link = await db.deep_links.find_one({"short_url": short_url})
    return RedirectResponse(link["long_url"])


@app.post("/{short_url}")
async def udpate_short_url(short_url: str, new_long_url: Annotated[str, Form()]):
    old_link = await db.deep_links.find_one({"short_url": short_url})
    update_result = await db.deep_links.update_one({"_id": old_link["_id"]}, {"$set": {"long_url": new_long_url}})
    if update_result["acknowledged"]:
        new_link = await db.deep_links.find_one({"short_url": short_url})
        return {"short_url": new_link["short_url"], "long_url": new_link["long_url"]}
    return {"error": "something went wrong"}


@app.get("/", response_class=HTMLResponse)
async def index():
    return """
    <html>
        <head>
            <title>Some HTML in here</title>
        </head>
        <body>
            <form action="/" method="post">
                <label for="long_url">URL to add:</label><br>
                <input type="text" id="long_url" name="long_url" value="https://www.google.com"><br>
                <label for="short_url">short_url:</label><br>
                <input type="text" id="short_url" name="short_url" value=""><br>
                <input type="submit" value="Go" />
            </form>
        </body>
    </html>
    """


def get_key_by_value(dict_obj, value_to_find):
    for key, value in dict_obj.items():
        if value == value_to_find:
            return key
    return None
