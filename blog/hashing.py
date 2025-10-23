from passlib.context import CryptContext

pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Hash():
    @staticmethod
    def bcrypt(password: str):
        return pwd.hash(password)