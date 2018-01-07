from urllib import request,parse
from PIL import Image,ImageDraw
import requests
import requests
import base64
import json
import os


# 获取图片的base64
def getImageBase64(filePath):
    with open(filePath,'rb') as f:
        data_base64 = base64.b64encode(f.read())
        return data_base64

# 人脸检测
def detectFace(filePath):
    url = 'https://api-cn.faceplusplus.com/facepp/v3/detect'
    base64_image = getImageBase64(filePath)
    str_base64_image = str(base64_image, encoding='utf-8')

    values = {
        'api_key': 'uA1y6yThFXx---noxjaff95aV2jROhbi',
        'api_secret': 'nVWe98cAGJ8q9d0Qn30IoKoaPfAPj8k_',
        'image_base64':str_base64_image,
        'return_attributes':'gender,age,smiling,emotion'
    }
    response = requests.post(url,data=values)
    return json.loads(response.content)


#相片导出
def exportPhoto(imageName,faces):
    baseName = os.path.basename(imageName)
    img = Image.open(imageName)
    draw_instance = ImageDraw.Draw(img)
    hasSmile = False
    count = 0
    for item in faces:
        count = count + 1
        try:
            x = item['face_rectangle']['left']
            y = item['face_rectangle']['top']
            width = item['face_rectangle']['width']
            height = item['face_rectangle']['height']

            if item['attributes']['smile']['value'] >= item['attributes']['smile']['threshold']:
                draw_instance.rectangle((x,y, width+x, height+y), outline=(0, 255, 0))
                hasSmile = True
                Image.open(imageName).crop((x,y, width+x, height+y)).save('./temp/cropface/'+ str(count)+'_'+baseName)
        except:
            print('图片导出失败')
    if hasSmile:
        img.save('./temp/drawfaces/' + baseName)

if __name__ ==  '__main__':
    rootDir = './images/'
    list = os.listdir(rootDir)
    for item in list:
        try:
            response = detectFace(rootDir+item)
            if response.get('error_message') is None:
                exportPhoto(rootDir+item,response['faces'])
                print('success')
            else:
                print('error_message:'+response['error_message'])
        except:
            print('face++脸部识别异常')
