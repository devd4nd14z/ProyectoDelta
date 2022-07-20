from .entities.User import User

class UserModel():

    #Obtener los datos de un usuario a partir de su ID de usuario
    def getById(self, db, id):
        try: 
            cursor = db.connection.cursor()
            sql = """SELECT id, username, fullname FROM users WHERE id = {}""".format(id)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                return User(row[0], row[1], None, row[2])
            else:
                return None    
        except Exception as ex:
            raise Exception(ex) #Volver a lanzar la excepcion

    @classmethod #Se puede utilizar el metodo sin instanciar la clase
    def login(self, db, user):
        try: 
            cursor = db.connection.cursor()
            sql = """SELECT id, username, password, fullname 
                     FROM users 
                     WHERE username = '{}'""".format(user.username)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                user = User(row[0], row[1], User.validatePassword(row[2], user.password))
                return user
            else:
                return None    
        except Exception as ex:
            raise Exception(ex) #Volver a lanzar la excepcion