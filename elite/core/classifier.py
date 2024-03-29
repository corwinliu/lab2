#coding utf-8

import math
import codecs
from myutils import mread
from myutils import mread_init
from myutils import prandom_init
from myutils import prandom

LABEL_FN = "label/"
CLASSIFY_FN = "classify.txt"

def classify(result):
	age = result['age']
# 0: female, 1: male -> 2: female, 1: male
	gender = int(2.5 - result['sex'])
# a feature-value list for convenience of coding
	fvl = []
# facevalue is in [0, 1]
	facevalue = result['beauty']
	fvl.append(facevalue)
# value for beard is in [0, 1]
	beard = result['beard']
	fvl.append(beard)
# value for mustache is in [0, 1]
	mustache = result['mustache']
	fvl.append(mustache)
# value for glass is in [0, 1]
	glass = result['glasses']
	fvl.append(glass)
# value for sunglass is in [0, 1]
	sunglass = result['sunglasses']
	fvl.append(sunglass)
# value for eyeclosed is in [0, 1]
	eyeclosed = result['eye_closed']
	fvl.append(eyeclosed)
# value for mouthopen is in [0, 1]
	mouthopen = result['mouth_open_wide']
	fvl.append(mouthopen)
# value for each emotion is in [0, 1]
	emotion = result['emotion']
	em_name = ['happy', 'angry', 'sad', 'confused', 'disgust', 'surprised', 'calm']
	em_val = [0, 0, 0, 0, 0, 0, 0]
	for em in emotion:
		for i in range(0, len(em_name)):
			if em_name[i] == em:
				em_val[i] = emotion[em]
	for i in range(0, len(em_val)):
		fvl.append(em_val[i])

# value for random is in [0, 5]
# a pseudo-random number is generated based on the attribute 'smile'
	smile = result['smile'] * 100 + 2
	for i in range(0, int(smile)):
		prandom()
	fvl.append(0)

	fn = codecs.open(CLASSIFY_FN, "r", "utf-8")

	mread_init()
	n = int(mread(fn))
	attr = []
	for i in range(0, n):
		attr_name = mread(fn)
		m = int(mread(fn))

		if m == -1:
			# the pidx in 'classify.txt' starts from 1
			pidx = int(mread(fn)) - 1
			attr.append((attr_name, attr[pidx][1], i + 1))
			continue

		val = 0

		# valid age interval
		valid_age = 0
		for j in range(0, m):
			l = int(mread(fn))
			r = int(mread(fn))
			a = float(mread(fn))
			b = float(mread(fn))

			if not ((l >= 0 and age < l) or (r >= 0 and age > r)):
				valid_age = 1
				val = a * age + b

		if valid_age == 0:
			attr.append((attr_name, 0, i + 1))
			for j in range(0, 16):
				mread(fn)
			continue

		# gender restriction
		valid_gender = int(mread(fn))
		if valid_gender > 0 and valid_gender != gender:
			attr.append((attr_name, 0, i + 1))
			for j in range(0, 15):
				mread(fn)
			continue

		# computing score for each feature
		sum = 0

		if (i == 2):
			print val
		for j in range(0, 15):
			p = float(mread(fn))
			sum += abs(p)
			val += fvl[j] * p

		attr.append((attr_name, val, i + 1))

	best_attr = attr[0]
	index  = 0
	for i in range(1, n):
		if best_attr[1] < attr[i][1]:
			best_attr = attr[i]
			index = i

	print "----------------------------"

	attr.sort(key=lambda tup: -tup[1])

	ed = n
	for i in range(1, n):
		if abs(attr[i][1] - attr[i - 1][1]) >= 0.0001:
			ed = i - 1
			break
	# select a random attribute from similar attributes
	rand = int(prandom() * (ed + 1))
	temp = attr[0]
	attr[0] = attr[rand]
	attr[rand] = temp


	fn.close()

	return attr
	return LABEL_FN + str(index + 1) + ".png"
