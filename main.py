from typing import Optional

from fastapi import FastAPI

from pydantic import BaseModel
import uvicorn

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    is_offer: Optional[bool] = None

@app.get("/")
def read_root():
    return {"Hello": "World"}



@app.get('/blog')
def index(limit,published=True, sort:Optional[int]=None):
    if published:
        return {'data':f' the count of published blog is:{limit}{sort} '}
    else:
        return {'data':f' the count of blog list is:{limit}'}


@app.get("/items/unpublished")
def unpublished():
    return {"data": 'unpublished data'}

@app.get("/items/{item_id}")
def read_item(item_id:int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}



@app.put("/items/{item_id}")
def update_item(item_id: int,item:Item):

    print("Hello to my world")
    print("Hello every body")
    return {"item_name": item.name, "item_id": item_id}
    #return {"item_name": "Hello"}


# if __name__=='__main__':
#     uvicorn.run(app,host='localhost',port=5000)
