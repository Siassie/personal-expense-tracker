from bcrypt import hashpw, gensalt, checkpw

class HashHelper(object):

    @staticmethod
    def verify_password(plain_text : str, hashed_password):
        
        if checkpw(plain_text.encode('utf-8'), hashed_password.encode('utf-8')):
            return True
        
        else:
            return False
        

    @staticmethod
    def hash_password(plain_text : str):
        return hashpw(plain_text.encode('utf-8'), gensalt()).decode('utf-8')