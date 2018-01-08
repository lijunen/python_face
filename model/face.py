import uuid
import model.base #注意，这里导入的仅仅是模块，即文件！
class FaceModel(model.base.BaseModel): #要继承类，必须给类名前加模块名即模块名.类名
    def listFace(self):
        return self.db.fecth_all("select * from face")

    def saveFace(self,params):
        guid = str(uuid.uuid4())
        params['guid'] = guid
        return self.db.insert('face',params)



