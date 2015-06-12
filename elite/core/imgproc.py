# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import classifier
from myutils import outname
from random import random
from myutils import prandom
from myutils import prandom_init

LABEL_FN = "label/"
WINDOW_W = 120
WINDOW_H = 80
ABOVE_H = 10

def draw_single_box(img, draw, box, offset, text_img):
	h = int(box['size']['height'])
	w = int(box['size']['width'])
	x = int(box['tl']['x'] + offset['x'])
	y = int(box['tl']['y'] + offset['y'])
	draw.line([(x, y), (x + w, y), (x + w, y + h), (x, y + h), (x, y)],
			fill=(255,255,255), width = 1)

	ww = min(WINDOW_W, int(w * 1.8))
	wh = int(min(ww / float(text_img.size[0]) * text_img.size[1]
		, WINDOW_H))

	window = Image.new('RGBA', (ww * 2, wh + ABOVE_H),
				(0,0,0,0))
	px = 0 + window.size[0] / 2 - ww / 2
	py = (wh + ABOVE_H) - ABOVE_H;
	windraw = ImageDraw.Draw(window)
	windraw.polygon([(px, py), (px + ww / 2 - ABOVE_H, py),
			(px + ww / 2, wh + ABOVE_H),
			(px + ww / 2 + ABOVE_H, py),
			(px + ww, py), (px + ww, py - wh),
			(px, py - wh), (px, py)],
			fill=(255,255,255,192))
			#fill=(0,192,255,192))
	woff = (x + w / 2 - window.size[0] / 2, y - wh - ABOVE_H)

	img.paste(window, woff, mask=window)

	# ATTENTION! The value 1.2 here is a compensatory value for the
	# too small size of the word in the label picture
	r = max(text_img.size[0] / float(ww), text_img.size[1] / float(wh))
	rw = text_img.size[0] / r
	rh = text_img.size[1] / r
	attr_img = text_img.resize((int(rw * 1.2), int(rh * 1.2)))

	# So as the value 0.6 (0.6 = 1.2 / 2)
	img.paste(attr_img, (int(x + w * 0.5 - rw * 0.6),
			     int(y - wh - ABOVE_H + wh * 0.5 - rh * 0.6)),
			     mask=attr_img)

	return img


def draw_box(img, result):
	img_w, img_h = img.size

	# calculate the tightest valid boundary for this image
	tvb_x1 = 0	# for width
	tvb_x2 = 0
	tvb_y1 = 0	# for height
	tvb_y2 = 0
	for i in range(0, len(result)):
		rbtx = result[i]['boundingbox']['tl']['x']
		rbty = result[i]['boundingbox']['tl']['y']
		rbsw = result[i]['boundingbox']['size']['width']
		rbsh = result[i]['boundingbox']['size']['height']
		tvb_y1 = max(tvb_y1, -(rbty - ABOVE_H - WINDOW_H))
		tvb_x1 = max(tvb_x1, -(rbtx + rbsw / 2 - WINDOW_W / 2))
		tvb_x2 = max(tvb_x2, rbtx + rbsw / 2 + WINDOW_W / 2 - img_w)

	bg = Image.new('RGBA', (int(img_w + tvb_x1 + tvb_x2),
				int(img_h + tvb_y1)),
			(255,255,255,255))
	bg_w, bg_h = bg.size
	offset = (int(tvb_x1), int(tvb_y1))
	bg.paste(img, offset)
	img = bg
	offset = {'x': offset[0], 'y': offset[1]}

	draw = ImageDraw.Draw(img)

	prandom_init()
	attrs = []
	for i in range(0, len(result)):
		attrs.append(classifier.classify(result[i]))

	# A algorithm to assure the diversity of attributes:
	# 	if there are multiple same attributes, select one of them,
	# 	change the attributes of the corresponding people to a
	#	secondary attributes. Repeat.
	np = len(result)
	ca = []
	for i in range(0, np):
		ca.append(0)
	while True:
		'''
		print "======================"
		for i in range(0, np):
			print attrs[i][ca[i]][0]
		print "======================="
		'''
		stop = True
		for i in range(0, np):
			# get the index of the best attribute
			idxi = attrs[i][ca[i]][2]
			eq = [i]
			for j in range(i + 1, np):
				idxj = attrs[j][ca[j]][2]
				if idxi == idxj:
					eq.append(j)
			if len(eq) > 1:
				s = int(prandom() * len(eq))
				ca[eq[s]] += 1
				stop = False
				break
		if stop:
			break

	for i in range(0, len(result)):
		text_fn = LABEL_FN + str(attrs[i][ca[i]][2]) + ".png"
		img = draw_single_box(img, draw, result[i]['boundingbox'],
					offset, Image.open(text_fn))
	return img
