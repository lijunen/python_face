from urllib import request,parse
from PIL import Image,ImageDraw
import requests
import requests
import base64
import json
import os
from model.face import FaceModel

def getImageBase64(filePath):
    '''
    获取图片的base64
    :param filePath:
    :return:
    '''
    with open(filePath,'rb') as f:
        try:
            data_base64 = base64.b64encode(f.read())
            return data_base64
        except:
            return ''

def detectFace(filePath):
    '''
    人脸检测
    :param filePath:
    :return:
    '''
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

def exportPhoto(imageName,faces):
    '''
    相片导出
    :param imageName:
    :param faces:
    :return:
    '''
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
                crop_face_image = './temp/cropface/'+ str(count)+'_'+baseName
                draw_face_image = './temp/drawfaces/' + baseName
                Image.open(imageName).crop((x,y, width+x, height+y)).save(crop_face_image)
                #入库
                saveFaces(item,imageName,crop_face_image,draw_face_image)
        except:
            print('图片导出失败')
    if hasSmile:
        img.save('./temp/drawfaces/' + baseName)

def saveFaces(item,original_image,crop_face_image,drap_face_image):
    face_model = FaceModel()
    params = {
        'face_token': item['face_token'],
        'original_image': str(getImageBase64(original_image),encoding='utf-8'),
        'crop_face_image': str(getImageBase64(crop_face_image),encoding='utf-8'),
        'drap_face_image': str(getImageBase64(drap_face_image),encoding='utf-8'),
        'gender': item['attributes']['gender']['value'],
        'age': item['attributes']['age']['value'],
        'emotion': json.dumps(item['attributes']['emotion']),
        'face_rectangle': json.dumps(item['face_rectangle']),
        'beauty': 0,
        'skinstatus': '',
        'smile': item['attributes']['smile']['value']
    }

    face_model.saveFace(params)


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
