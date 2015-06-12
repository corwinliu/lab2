#coding utf-8
FACEPP_KEY = '5d6e636245ebcac64710ea947d9c3a52'
FACEPP_SECRET = 'DWzjsy2dNcLGaoOayWgR2JtnpSZw6uoA'
ReKognition_API_KEY = '8RRuJV77BxrooG4F'
ReKognition_API_SECRET = 'sDvjMyWgqFfTDDpo'

import math
import os
import time
import requests
import imgproc
import base64
import json
from PIL import Image
from PIL import ExifTags
from myfacepp import API, File
from myutils import outname
from pprint import pformat

def print_result(hint, result):
	def encode(obj):
		if type(obj) is unicode:
			return obj.encode('utf-8')
		if type(obj) is dict:
			return {encode(k): encode(v) for (k, v) in obj.iteritems()}
		if type(obj) is list:
			return [encode(i) for i in obj]
		return obj
	print hint
	result = encode(result)
	print '\n'.join(['  ' + i for i in pformat(result, width = 75).split('\n')])

def facepp(api, PERSONS):
	# Step 1: Create a group to add these persons in
	api.group.create(group_name = 'test')

	keyp = []
	# Step 2: Detect faces from those images and add them to the persons
	for (name, fn) in PERSONS:
		result = api.detection.detect(post = True,
					img = File(fn), mode = "normal")
		print_result('Detection result for {}:'.format(name), result)
		pl = []
		for i in range(0, len(result['face'])):
			pl.append(result['face'][i]['position']['nose'])
		keyp.append((name, pl))
	return keyp


def elimit_wrong(name, keyp, result):
	for (kname, knl) in keyp:
		if (kname == name):
			nl = knl
			break
	img_h = result['ori_img_size']['height']
	img_w = result['ori_img_size']['width']
	rm = []
	for i in range(0, len(result['face_detection'])):
		box = result['face_detection'][i]['boundingbox']
		h = box['size']['height'] / float(img_h) * 100
		w = box['size']['width'] / float(img_w) * 100
		x1 = box['tl']['x'] / float(img_w) * 100
		y1 = box['tl']['y'] / float(img_h) * 100

		isFace = False
		for j in range(0, len(nl)):
			x = nl[j]['x']
			y = nl[j]['y']
			if x1 <= x and x1 + w >= x and y1 <= y and y1 + h >= y:
				isFace = True
				break
		if isFace == False:
			rm.append(i)

	for e in reversed(rm):
		result['face_detection'].pop(e)

	return result


def reKognition(PERSONS_FILE, keyp):
	for (name, fn) in PERSONS_FILE:
		# upload image and get analysis result
		with open(fn, "rb") as image_file:
			encoded_string = base64.b64encode(image_file.read())
		json_resp = requests.post("http://rekognition.com/func/api/",
			data = { 'api_key'	: ReKognition_API_KEY,
				 'api_secret'	: ReKognition_API_SECRET,
				 'jobs'		: 'face_part_detail_gender_age_emotion_race_glass_mouth_open_wide_eye_closed_mustchae_beard_sunglasses_recognize_beauty',
				 'base64'	: encoded_string}
		)
		result = json.loads(json_resp.text)

		print_result("", result)

		# elimit inaccurately detected face
		result = elimit_wrong(name, keyp, result)

		# modify the original image
		img = Image.open(fn)
		img = imgproc.draw_box(img, result['face_detection'])
		return img
#		img.save(outname(fn, 'png'), 'PNG')

def exif_process(img, fw):
	# pre-process for EXIF orientation information
	if (img._getexif() == None):
		return img
	exif = dict((ExifTags.TAGS[k], v) for k, v in img._getexif().items() if k in ExifTags.TAGS)
	ore = exif['Orientation']
	if ore == 2:
		# Vertical Mirror
		img = img.transpose(Image.FLIP_LEFT_RIGHT)
        elif ore == 3:
		# Rotation 180
		img = img.transpose(Image.ROTATE_180)
        elif ore == 4:
		# Horizontal Mirror
		img = img.transpose(Image.FLIP_TOP_BOTTOM)
        elif ore == 5:
		# Horizontal Mirror + Rotation 90 CCW
		if (fw):
			img = img.transpose(Image.FLIP_TOP_BOTTOM).transpose(Image.ROTATE_90)
		else:
			img = img.transpose(Image.ROTATE_270).transpose(Image.FLIP_TOP_BOTTOM)
        elif ore == 6:
		# Rotation 270
		if (fw):
			img = img.transpose(Image.ROTATE_270)
		else:
			img = img.transpose(Image.ROTATE_90)
        elif ore == 7:
		# Horizontal Mirror + Rotation 270
		if (fw):
			img = img.transpose(Image.FLIP_TOP_BOTTOM).transpose(Image.ROTATE_270)
		else:
			img = img.transpose(Image.ROTATE_90).transpose(Image.FLIP_TOP_BOTTOM)
        elif ore == 8:
		# Rotation 90
		if (fw):
			img = img.transpose(Image.ROTATE_90)
		else:
			img = img.transpose(Image.ROTATE_270)
	return img

def process(img):
	original_img = img
	img = exif_process(img, True)
	if (img.size[0] * img.size[1] >= 200000):
		r = math.sqrt(img.size[0] * img.size[1] / 200000.0)
		img = img.resize((int(img.size[0] / r), int(img.size[1] / r)))
	img.save('tmp.png')

	PERSONS_FILE = [
	#	('Obama', 'Obama1.jpg'),
	#	('Baby', 'sad_smile.jpg'),
	#	('Friend', 'friends.jpg'),
	#	('Disgust', 'disgust.jpg'),
	#	('Fear', 'fear2.jpg'),
	#	('Family', 'family.jpg')
		('TEMP', 'tmp.png')
	]

	#face++ api
	api = API(FACEPP_KEY, FACEPP_SECRET)
	try:
		keyp = facepp(api, PERSONS_FILE)
	finally:
		try:
			api.group.delete(group_name = 'test')
		finally:
			pass

	# api of ReKognition
	return reKognition(PERSONS_FILE, keyp)

#process(Image.open('bug_data/image_yCrSrDn.jpg')).save("bug_data/out.png")
'''
for i in range(0, 60):
	print i
	if not os.path.isfile('../old/train/' + str(i) + '.jpg'):
		continue
	process(Image.open('../old/train/' + str(i) + '.jpg')).save("../old/train_res/" + str(i) + "_out.png")
'''
