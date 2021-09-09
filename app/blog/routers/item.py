from fastapi import APIRouter
from fastapi import FastAPI, Depends,status,Response,HTTPException

from sqlalchemy.orm import Session

from typing import List
from .. import schemas,models,database,oauth2

router = APIRouter(
            tags=["blog"],

)


@router.get('/blog',response_model = List[schemas.ShowBlog])
def get_all(db:Session=Depends(database.get_db),current_user:schemas.User=Depends(oauth2.get_current_user)):
    blogs = db.query(models.Item).all()
    return blogs


@router.post('/blog',status_code=status.HTTP_201_CREATED, tags=["blog"])
def create(request:schemas.Blog, db:Session=Depends(database.get_db),current_user:schemas.User=Depends(oauth2.get_current_user)):
    new_blog = models.Item(title=request.title, body=request.body,owner_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@router.get('/blog/{id}',status_code = status.HTTP_200_OK,response_model = schemas.ShowBlog)
def show(id,response:Response,db:Session=Depends(database.get_db),current_user:schemas.User=Depends(oauth2.get_current_user)):
    blog = db.query(models.Item).filter(models.Item.id == id).first()
    user = db.query(models.User).filter(models.User.id == blog.owner_id).first()
    if not blog:
        #response.status_code = HTTP_404_NOT_FOUND
        #return {'detail':f'ID {id} isn\'t available'}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'ID {id} isn\'t available')
    return blog #{'title':blog.title,'body':blog.body,'owner':user.name}


@router.delete('/blog/{id}',status_code=status.HTTP_200_OK, tags=["blog"])
def delete(id,db:Session=Depends(database.get_db),current_user:schemas.User=Depends(oauth2.get_current_user)):
    blog = db.query(models.Item).filter(models.Item.id ==id)#.delete()
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'ID {id} isn\'t available')
    blog.delete()
    db.commit()

    return "Done"

@router.put('/blog/{id}',status_code=status.HTTP_202_ACCEPTED, tags=["blog"])
def put(id,request:schemas.Blog,db:Session=Depends(database.get_db),current_user:schemas.User=Depends(oauth2.get_current_user)):
    # blog = db.query(models.Item).filter(models.Item.id ==id).first()
    # if not blog:
    #     raise HTTPException(status_code=HTTP_404_NOT_FOUND,detail=f'ID {id} isn\'t available')
    # blog.title = request.title
    # blog.description = request.body
    blog = db.query(models.Item).filter(models.Item.id ==id)#.update({'title':request.title,  \
                                                                  #'description':request.body})
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'ID {id} isn\'t available')
    blog.update({'title':request.title,  \
                 'body':request.body})

    db.commit()
    return "Done"