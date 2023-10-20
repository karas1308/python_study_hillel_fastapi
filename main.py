import hashlib
from typing import Annotated, Optional

from bson import ObjectId
from fastapi import Depends, FastAPI, Form, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, Field

from common import create_short_url, get_long_url
from mongo_db import db

app = FastAPI()


def fake_hash_password(password: str):
    # return "fakehashed" + password
    return hashlib.md5(password.encode("utf-8"))


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    id: str = Field(alias='_id')
    hashed_password: str


async def get_user_by_token(token: str):
    user_dict = await db.users.find_one({"_id": ObjectId(token)})
    if user_dict:
        user_dict["_id"] = str(user_dict["_id"])
        return UserInDB(**user_dict)


async def fake_decode_token(token):
    user = await get_user_by_token(token)
    return user


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = await fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(
        current_user: Annotated[User, Depends(get_current_user)]
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_dict = await db.users.find_one({"username": form_data.username})
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user_dict["_id"] = str(user_dict["_id"])
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password).hexdigest()
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = str(user_dict["_id"])
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me")
async def read_users_me(
        current_user: Annotated[User, Depends(get_current_active_user)]
):
    return current_user


@app.post("/")
async def root(current_user: Annotated[User, Depends(get_current_active_user)],
               long_url: Annotated[str, Form()],
               short_url: Optional[str] = Form(None)):
    short_url = await create_short_url(long_url, short_url, user_id=current_user.id)
    return short_url


@app.get("/{short_url}")
async def to_long(short_url: str):
    long_url = await get_long_url(short_url)
    data = await db.deep_links.find_one({"short_url": short_url})
    await db.redirects.insert_one({"short_url": short_url, "owner": data["user_id"]})
    return RedirectResponse(long_url)


@app.post("/{short_url}")
async def update_short_url(current_user: Annotated[User, Depends(get_current_active_user)],
                           short_url: str, new_long_url: Annotated[str, Form()]):
    old_link = await db.deep_links.find_one({"short_url": short_url})
    if old_link.get("user_id") and current_user.id != old_link.get("user_id"):
        return {"error": "Operation is not allowed. Wrong owner"}
    data = {"long_url": new_long_url}
    if not old_link.get("user_id"):
        data["user_id"] = current_user.id
    update_result = await db.deep_links.update_one({"_id": old_link["_id"]}, {"$set": data})
    if update_result.acknowledged:
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
