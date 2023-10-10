import uuid
from typing import Annotated

from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, RedirectResponse

app = FastAPI()

dict_urls = {
}


@app.post("/")
async def root(long_url: Annotated[str, Form()]):
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
                <input type="text" name="long_url" value="https://www.google.com" />
                <input type="submit" value="Go" />
            </form>
        </body>
    </html>
    """
