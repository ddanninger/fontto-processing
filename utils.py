#!/usr/bin/python3
# -*- coding: utf-8 -*-

import urllib
import urllib.request
from PIL import Image
from io import BytesIO
import base64
import boto3


def url2img(input_address):
    """
    - fontto_pix2pix에서 사용할 수 있도록 url을 통해 이미지를 로드하고 PIL Image로 변환하여 반환
    - 입력 : url
    - 반환 : image
    """
    # url -> bytes
    url = urllib.parse.urlsplit(input_address)
    url = list(url)
    url[2] = urllib.parse.quote(url[2])
    url = urllib.parse.urlunsplit(url)
    url = urllib.request.urlopen(url).read()
    bytesFromS3 = BytesIO(url)
    # bytes -> image
    input_PIL = Image.open(bytesFromS3)

    return input_PIL


def store2S3(env, filetype, userID, count, uni, upload_file):
    if filetype == 'bitmaps':
        #PIL to buffer
        buffer = BytesIO()
        upload_file.save(buffer, format='JPEG')
        upload_file = base64.b64encode(buffer.getvalue())

        contenttype = 'image/jpeg'
        body = base64.b64decode(upload_file)
    elif filetype == 'vectors':
        upload_file = open(upload_file, 'rb')

        contenttype = 'image/svg+xml'
        body = upload_file
    #just in case saving 'JPEG' file
    elif filetype == 'JPEG':
        upload_file = open(upload_file, 'rb')

        contenttype = 'image/jpeg'
        body = upload_file

    s3key = '%s/outputs/%s/%s/%s/%s' % (env, filetype, userID, count, uni)
    s3 = boto3.resource('s3')
    s3.Bucket('fontto').put_object(
        Key=s3key, Body=body, ContentType=contenttype, ACL='public-read')
    full_address = 'https://s3.ap-northeast-2.amazonaws.com/fontto/' + s3key
    return full_address


def ttf2S3(env, userID, count, ttf_converted):
    contenttype = 'font/ttf'
    body = ttf_converted

    s3key = '%s/outputs/ttf/%s/%s' % (env, userID, count)
    s3 = boto3.resource('s3')
    s3.Bucket('fontto').put_object(
        Key=s3key, Body=body, ContentType=contenttype, ACL='public-read')
    ttf_address = 'https://s3.ap-northeast-2.amazonaws.com/fontto/' + s3key
    return ttf_address
