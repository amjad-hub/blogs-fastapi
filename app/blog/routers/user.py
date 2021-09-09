from fastapi import APIRouter
from fastapi import FastAPI, Depends,status,Response,HTTPException

from sqlalchemy.orm import Session

from typing import List
from .. import schemas,models,database
router = APIRouter(
        tags=["users"],

)
from passlib.context import CryptContext



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)


@router.post('/user', status_code = status.HTTP_201_CREATED,response_model = schemas.ShowUser)
def create_user(request:schemas.User, db:Session = Depends(database.get_db)): 
    new_user = models.User(name = request.name, \
                            email = request.email,\
                            hashed_password = get_password_hash(request.password))
    #new_user = models.User(request)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.get('/user', status_code = status.HTTP_200_OK,response_model = List[schemas.ShowUser])
def get_users(db:Session = Depends(database.get_db)): 
    users = db.query(models.User).all()

    return users


@router.get('/user/{id}', status_code = status.HTTP_200_OK,response_model = schemas.ShowUser)
def get_user(id,db:Session = Depends(database.get_db)): 
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'User with ID: {id} isn\'t exist')

    return user