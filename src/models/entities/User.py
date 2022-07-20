from werkzeug.security import check_password_hash
#from werkzeug.security import generate_password_hash
from flask_login import UserMixin


class User(UserMixin):

    def __init__(self, id, username, password, fullname=""):
        self.id = id
        self.username = username
        self.password = password
        self.fullname = fullname

    #@classmethod: anotacion para hacer que se pueda utilizar el metodo sin necesidad de instanciar la clase
    @classmethod
    def validatePassword(self, hashed_password, password):
        return check_password_hash(hashed_password, password)


#print(generate_password_hash("admin"))

