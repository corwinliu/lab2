API_KEY = '5d6e636245ebcac64710ea947d9c3a52'
API_SECRET = 'DWzjsy2dNcLGaoOayWgR2JtnpSZw6uoA'
FACE2_API_KEY = 'f10b684b762c4ee49e14f2ae42eb1909'
FACE2_CLIENT_ID = '402aef1d19544d2eb17c8653eff0a55b'
ReKognition_API_KEY = '8RRuJV77BxrooG4F'
ReKognition_API_SECRET = 'sDvjMyWgqFfTDDpo'

import time
import requests
import imgproc
import base64
import json
from pprint import pformat
from myfacepp import API, File

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

	# Step 2: Detect faces from those images and add them to the persons
	for (name, fn) in PERSONS:
		result = api.detection.detect(post = True,
					img = File(fn), mode = "oneface")
		print_result('Detection result for {}:'.format(name), result)

		face_id = result['face'][0]['face_id']

		api.person.create(person_name = name, group_name = 'test',
				face_id = face_id)
		result = api.detection.landmark(face_id = face_id)
#		print_result("Landmark result for {}".format(name), result)

		imgproc.smile(fn, result['result'][0]['landmark'])

	# Step 3: Train the group
'''	result = api.recognition.train(group_name = 'test', type = 'all')

	print_result('Train result:', result)

	session_id = result['session_id']
'''
	# Wait before train completes
'''	while True:
		result = api.info.get_session(session_id = session_id)
		if result['status'] == u'SUCC':
			print_result('Async train result:', result)
			break
		time.sleep(1)
'''
	# Step 4: Recognize the unknown face image
	# ...


def face2(PERSONS_FILE):
	for (name, fn) in PERSONS_FILE:
		json_resp = requests.post('http://api.sightcorp.com/api/detect/',
			data =	{ 'app_key'	: FACE2_API_KEY,
				  'client_id'	: FACE2_CLIENT_ID},
			files =	{ 'img'		: ('filename', open(fn, 'rb'))}
		)
		print "Response : ", json_resp.text


def reKognition(PERSONS_FILE):
	for (name, fn) in PERSONS_FILE:
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
		imgproc.draw_box(fn, result['face_detection'][0]['boundingbox']);

# In the released version, the address should be a variable, an argument
# from input.
PERSONS_URL = [
	('Obama', 'http://a.hiphotos.baidu.com/baike/c0%3Dbaike80%2C5%2'
		  'C5%2C80%2C26/sign=72b7f7380a24ab18f41be96554938da8/f'
		  '7246b600c338744cb293d62520fd9f9d72aa03b.jpg')
]

PERSONS_FILE = [
#	('Obama', 'Obama1.jpg')
#	('Baby', 'sad_smile.jpg')
	('Friend', 'friends.jpg')
#	('Disgust', 'disgust.jpg')
#	('Fear', 'fear2.jpg')
#	('Neutral', 'neutral.gif')
]


# api of FACE++
'''
api = API(API_KEY, API_SECRET)
try:
	facepp(api, PERSONS_FILE)
finally:
	api.group.delete(group_name = 'test')
	api.person.delete(person_name = [i[0] for i in PERSONS_FILE])
'''

# api of F.A.C.E
'''
face2(PERSONS_FILE)
'''

# api of ReKognition
reKognition(PERSONS_FILE)
