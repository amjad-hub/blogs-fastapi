import sqlalchemy
from .. import schemas,database,models,token
from sqlalchemy.orm import Session
from fastapi import Depends,HTTPException,status,APIRouter
from ..hashing import Hash
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


router = APIRouter(
    tags=['authentications'],
    #prefix='/auth',
)



@router.post('/login')
def login(request:OAuth2PasswordRequestForm = Depends(), db:Session=Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == request.username).first()
    h = Hash()
    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND , detail=f'user isn\'t available')
    if not h.verify(request.password, user.hashed_password):
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND , detail=f'password isn\'t correct')

    #access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = token.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}