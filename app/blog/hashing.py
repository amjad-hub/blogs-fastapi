

from passlib.context import CryptContext

class Hash():
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def bcrypt(self,password):
        return self.pwd_context.hash(password)

    def verify(self,plain_pass,hashed_pass):
        return self.pwd_context.verify(plain_pass,hashed_pass)
