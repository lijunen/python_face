import base #注意，这里导入的仅仅是模块，即文件！
class Face(base.BaseModel): #要继承类，必须给类名前加模块名即模块名.类名
    def listFace(self):
        return self.db.fecth_all("select * from face where guid =%s and face_token = %s",(1,1))

    def saveFace(self):
        return self.db.execute()


face = Face()
print(face.listFace())