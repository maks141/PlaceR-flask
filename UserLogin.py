class UserLogin():
    def fromBD(self, user_id, db):
        self.__user = db.getUser(user_id)
        return self
    
    def create(self, user):
        self.__user = user
        return self
    
    def is_authenticated(self):
        return True
    
    def if_active(self):
        return True
    
    def if_anonymous(self):
        return False
    
    def get_id(self):
        return str(self.__user['id'])