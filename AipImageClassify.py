from aip import AipFace
from PIL import Image,ImageDraw
import os
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

def listImage(filePath):
    list = os.listdir(filePath)
    for item in list:
        print(item)
        # os.path.split(item)


def detectFace(imageName):
    # """ 你的 APPID AK SK """
    APP_ID = '10619822'
    API_KEY = 'irGmTc3RGbOZWs9ztcxt2L9g'
    SECRET_KEY = 'Yt8SbchlWIgHL8ofx0a3WwywVqYRZsRl'

    client = AipFace(APP_ID, API_KEY, SECRET_KEY)
    baseName = os.path.basename(imageName)
    image = get_file_content(imageName)
    client.detect(image);
    # """ 如果有可选参数 """
    options = {}
    options["max_face_num"] = 20
    options["face_fields"] = "age,expression"
    # """ 带参数调用人脸检测 """
    res = client.detect(image, options)
    img = Image.open(imageName)
    draw_instance = ImageDraw.Draw(img)
    hasSmile = False
    for item in res['result']:
        print(item)
        try:
            if item['expression']:
                draw_instance.rectangle((item['location']['left'],item['location']['top'], item['location']['width']+item['location']['left'], item['location']['height']+item['location']['top']), outline=(0, 255, 0))
                hasSmile = True
                Image.open(imageName).crop((item['location']['left'],item['location']['top'], item['location']['width']+item['location']['left'], item['location']['height']+item['location']['top'])).save('./temp/cropface/'+ baseName)
        except:
            print('error')

    if hasSmile:
        img.save('./temp/drawfaces/' + baseName)




if __name__ == '__main__':
    rootDir = './images/'
    list = os.listdir(rootDir)
    for item in list:
        detectFace(rootDir+item)

