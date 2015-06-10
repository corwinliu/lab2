#coding utf-8

import math
import codecs
from myutils import mread
from myutils import mread_init

LABEL_FN = "label/"
CLASSIFY_FN = "classify.txt"

def classify(result):
	age = result['age']
# 0: female, 1: male -> 2: female, 1: male
	gender = 2 - result['sex']
# a feature-value list for convenience of coding
	fvl = []
# facevalue is in [0, 10]
	facevalue = result['beauty'] * 10
	fvl.append(facevalue)
# value for beard is in [0, 10]
	beard = result['beard'] * 10
	fvl.append(beard)
# value for mustache is in [0, 10]
	mustache = result['mustache'] * 10
	fvl.append(mustache)
# value for glass is in [0, 10]
	glass = result['glasses'] * 10
	fvl.append(glass)
# value for sunglass is in [0, 10]
	sunglass = result['sunglasses'] * 10
	fvl.append(sunglass)
# value for eyeclosed is in [0, 10]
	eyeclosed = result['eye_closed'] * 10
	fvl.append(eyeclosed)
# value for mouthopen is in [0, 10]
	mouthopen = result['mouth_open_wide'] * 10
	fvl.append(mouthopen)
# value for each emotion is in [0, 10]
	emotion = result['emotion']
	em_name = ['happy', 'angry', 'sad', 'confused', 'disgust', 'surprised', 'calm']
	em_val = [0, 0, 0, 0, 0, 0, 0]
	for em in emotion:
		for i in range(0, len(em_name)):
			if em_name[i] == em:
				em_val[i] = emotion[em] * 10
	for i in range(0, len(em_val)):
		fvl.append(em_val[i])

# value for random is in [0, 5]
# a pseudo-random number is generated based on the attribute 'smile'
#	smile = result['smile'] * 100 + 2
#	random = 1
#	for i in range(0, 10):
#		random = (random * smile) % 137
	random = 0#random / 137.0
	fvl.append(random)

	fn = codecs.open(CLASSIFY_FN, "r", "utf-8")

	mread_init()
	n = int(mread(fn))
	attr = []
	for i in range(0, n):
		attr_name = mread(fn)
		m = int(mread(fn))
		val = 0

		# valid age interval
		valid_age = 1
		for j in range(0, m):
			l = int(mread(fn))
			r = int(mread(fn))
			if (l >= 0 and age < l) or (r >= 0 and age > r):
				valid_age = 0
				break
		if valid_age == 0:
			attr.append((attr_name, val))
			for j in range(0, 16):
				mread(fn)
			continue

		# gender restriction
		valid_gender = int(mread(fn))
		if valid_gender > 0 and valid_gender != gender:
			attr.append((attr_name, val))
			for j in range(0, 15):
				mread(fn)
			continue

		# computing score for each feature
		sum = 0
		for j in range(0, 15):
			p = float(mread(fn))
			sum += abs(p)
			val += fvl[j] * p
		val /= sum

		attr.append((attr_name, val))

	best_attr = attr[0]
	index  = 0
	for i in range(1, n):
		if best_attr[1] < attr[i][1]:
			best_attr = attr[i]
			index = i

	print "----------------------------"

	attr.sort(key=lambda tup: -tup[1])
#	for i in range(0, n):
#		print attr[i][0], attr[i][1]

	fn.close()

	return LABEL_FN + str(index + 1) + ".png"
