import uuid
import base #注意，这里导入的仅仅是模块，即文件！
class Face(base.BaseModel): #要继承类，必须给类名前加模块名即模块名.类名
    def listFace(self):
        return self.db.fecth_all("select * from face")

    def saveFace(self,params):
        guid = str(uuid.uuid4())
        params['guid'] = guid
        return self.db.insert('face',params)


face = Face()
print(face.listFace())
params = {
    'face_token':'22',
    'original_image':'22',
    'crop_face_image':'22',
    'drap_face_image':'22',
    'gender':'22',
    'age':'22',
    'emotion':'22',
    'face_rectangle':'22',
    'beauty':'22',
    'skinstatus':'22',
    'smile':11
}

flag = face.saveFace(params)
print(uuid.uuid4())