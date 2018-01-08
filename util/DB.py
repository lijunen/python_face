import pymysql

class DB(object):
    def __init__(self,db_host,db_port,db_user,db_password,db_name):
        self.__db_host = db_host
        self.__db_port = db_port
        self.__db_user = db_user
        self.__db_password = db_password
        self.__db_name = db_name
        self.__conn = None
        self.__cur = None
        self.connection()

    def connection(self):
        try:
            self.__conn = pymysql.connect(self.__db_host,self.__db_user,self.__db_password,self.__db_name,charset='utf8',cursorclass=pymysql.cursors.DictCursor)
            self.__cur = self.__conn.cursor()
        except:
            print('无法连接数据库')

    def fetch_one(self,sql,param = {}):
        try:
            self.__cur.execute(sql,(param))
            return self.__cur.fetchone()
        except:
            pass

    def fecth_all(self,sql,param={}):
        try:
            self.__cur.execute(sql,(param))
            return self.__cur.fetchall()
        except:
            print('sql error')
            pass

    def insert(self,table_name,params):
        try:
            for key in params:
                params[key] = "'"+str(params[key])+"'"
            key = ','.join(params.keys())
            values = ','.join(params.values())
            sql = "INSERT INTO "+table_name+"("+key+")VALUES("+values+")"
            print(sql)
            return self.__cur.execute(sql)
        except:
            print('error,sql:'+sql)
