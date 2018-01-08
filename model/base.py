import configparser
from util.DB import *
class BaseModel(object):
    def __init__(self):
        conf = configparser.ConfigParser()
        conf.read('./config/db.ini')
        localhost = conf.get('mysql','localhost')
        port = conf.get('mysql','port')
        db_user = conf.get('mysql','db_user')
        db_password = conf.get('mysql','db_password')
        db_name = conf.get('mysql','db_name')
        self.db = DB(localhost,port,db_user,db_password,db_name)
