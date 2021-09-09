from fastapi import FastAPI
from . import schemas,models
from .database import engine
from .routers import item, user,authentications



tags_metadata = [
    {
        "name": "users",
        "description": "Operations with users. The **login** logic is also here.",
    },
    {
        "name": "blog",
        "description": "Manage items. So _fancy_ they have their own docs.",
        "externalDocs": {
            "description": "Items external docs",
            "url": "https://fastapi.tiangolo.com/",
        },
    },
]


app = FastAPI(openapi_tags = tags_metadata)
models.Base.metadata.create_all(engine)

app.include_router(user.router)
app.include_router(item.router)
app.include_router(authentications.router)


