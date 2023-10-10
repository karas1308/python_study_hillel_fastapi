import uuid
from typing import Annotated

from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, RedirectResponse

app = FastAPI()

dict_urls = {
    "google": "https://www.google.com",
    "bbc": "https://www.bbc.com"

}


@app.post("/")
async def root(long_url: Annotated[str, Form()]):
    if long_url.endswith(".ru"):
        return "ЗАБЛОКОВАНО"
    if long_url in dict_urls.values():
        short_url = get_key_by_value(dict_urls, long_url)
    else:
        short_url = str(uuid.uuid4())
        dict_urls[short_url] = long_url
    return short_url


@app.get("/{short_url}")
async def to_long(short_url: str):
    return RedirectResponse(dict_urls[short_url])


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
