# -*- coding: utf-8 -*-
import Image, ImageDraw, ImageFilter, ImageFont
from myutils import outname

def mark(fn, features):
	img = Image.open(fn)
	draw = ImageDraw.Draw(img)
	for (feature, pos) in features.iteritems():
		x = pos['x'] / 100.0 * img.size[0]
		y = pos['y'] / 100.0 * img.size[1]
		draw.rectangle([(x - 1, y - 1), (x + 1, y + 1)],
				outline=(0,0,255), fill=(0,0,0))
	img.save(outname(fn))

def drawDot(img, draw, feature):
	x = feature['x'] / 100.0 * img.size[0]
	y = feature['y'] / 100.0 * img.size[1]
	draw.rectangle([(x - 1, y - 1), (x + 1, y + 1)],
				outline=(0,0,255), fill=(0,0,0))

def drawLine(img, draw, feature1, feature2):
	x1 = feature1['x'] / 100.0 * img.size[0]
	y1 = feature1['y'] / 100.0 * img.size[1]
	x2 = feature2['x'] / 100.0 * img.size[0]
	y2 = feature2['y'] / 100.0 * img.size[1]
	draw.line([(x1, y1), (x2, y2)], fill=(0,0,255))

def gety(x, interval, features, img):
	minx = 10000
	maxx = 0
	for (p1, p2) in interval:
		x1 = features[p1]['x'] / 100.0 * img.size[0]
		x2 = features[p2]['x'] / 100.0 * img.size[0]
		if x1 < minx:
			minx = x1
		if x2 > maxx:
			maxx = x2

	for (p1, p2) in interval:
		x1 = features[p1]['x'] / 100.0 * img.size[0]
		x2 = features[p2]['x'] / 100.0 * img.size[0]
		if x1 == minx and x < minx:
			return features[p1]['y'] / 100.0 * img.size[1]
		if x2 == maxx and x > maxx:
			return features[p2]['y'] / 100.0 * img.size[1]
		if x1 <= x and x2 >= x:
			y1 = features[p1]['y'] / 100.0 * img.size[1]
			y2 = features[p2]['y'] / 100.0 * img.size[1]
			return (y2 - y1) / (x2 - x1) * (x - x1) + y1

def genrate(x, xl, xr):
	xm = (xl + xr) / 2.0
	ru = 1 - 0.3 / (xm - xl) * abs(x - xm)
	rd = 1 + 0.2 / (xm - xl) * abs(x - xm)
	return [ru, rd]

def smile(fn, features):
	img = Image.open(fn)
	draw = ImageDraw.Draw(img)
	MOUTHL = [('mouth_left_corner', 'mouth_lower_lip_left_contour2'),
		  ('mouth_lower_lip_left_contour2', 'mouth_lower_lip_left_contour3'),
		  ('mouth_lower_lip_left_contour3', 'mouth_lower_lip_bottom'),
		  ('mouth_lower_lip_bottom', 'mouth_lower_lip_right_contour3'),
		  ('mouth_lower_lip_right_contour3', 'mouth_lower_lip_right_contour2'),
		  ('mouth_lower_lip_right_contour2', 'mouth_right_corner')]
	MOUTHH = [('mouth_left_corner', 'mouth_upper_lip_left_contour1'),
		  ('mouth_upper_lip_left_contour1', 'mouth_upper_lip_left_contour2'),
		  ('mouth_upper_lip_left_contour2', 'mouth_upper_lip_top'),
		  ('mouth_upper_lip_top', 'mouth_upper_lip_right_contour2'),
		  ('mouth_upper_lip_right_contour2', 'mouth_upper_lip_right_contour1'),
		  ('mouth_upper_lip_right_contour1', 'mouth_right_corner')]

#	for (m1, m2) in MOUTHL + MOUTHH:
#		drawLine(img, draw, features[m1], features[m2])
	yuppb = int(features['contour_chin']['y'] / 100.0 * img.size[1])
	ylowb = int(features['nose_contour_lower_middle']['y'] / 100.0 * img.size[1])
	imgxl = int(features['mouth_left_corner']['x'] / 100.0 * img.size[0])
	imgxr = int(features['mouth_right_corner']['x'] / 100.0 * img.size[0])
	for x in range(imgxl, imgxr):
		imgyh = int(gety(x, MOUTHL, features, img))
		imgyl = int(gety(x, MOUTHH, features, img))
#		for y in range(imgyl, imgyh):
#			draw.point((x, y), fill=(0,0,255))
		rate = genrate(x, imgxl, imgxr)
		newyl = int((imgyl - ylowb) * rate[0] + ylowb)
		newyh = int(yuppb - (yuppb - imgyh) * rate[1])

		color = []
		for y in range(0, img.size[1]):
			color.append(img.getpixel((x, y)))
		for y in range(ylowb, newyl):
			cy = int((y - ylowb) / rate[0] + ylowb)
			draw.point((x, y), fill=color[cy])
		for y in range(newyl, newyh):
			cy = int((y - newyl) / float(newyh - newyl) * (imgyh - imgyl) + imgyl)
			draw.point((x, y), fill=color[cy])
		for y in range(newyh, yuppb):
			cy = int(yuppb - (yuppb - y) / rate[1])
			draw.point((x, y), fill=color[cy])

	img.save(outname(fn))

#	dbl = {}
#	dbl['nose_contour_lower_middle'] = features['nose_contour_lower_middle']
#	dbl['contour_chin'] = features['contour_chin']
#	mark('Obama1.jpg', dbl)

def draw_single_box(img, box):
	draw = ImageDraw.Draw(img)
	h = box['size']['height']
	w = box['size']['width']
	x = box['tl']['x']
	y = box['tl']['y']
	draw.line([(x, y), (x + h, y), (x + h, y + w), (x, y + w), (x, y)],
			fill=(0,0,255), width = 1)
	return img


def draw_box(img, result):
	for i in range(0, len(result)):
		img = draw_single_box(img, result[i]['boundingbox'])

	img_w, img_h = img.size
	bg = Image.new('RGBA', (int(img_w * 1.4), int(img_h * 1.4)),
			(0,128,255,255))
	bg_w, bg_h = bg.size
	offset = ((bg_w - img_w) / 2, (bg_h - img_h) / 2)
	bg.paste(img, offset)
	img = bg

	# compute the start line

	return img
