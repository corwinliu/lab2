# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import classifier
from myutils import outname

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

	ww = min(WINDOW_W, w)
	wh = int(min(ww / float(text_img.size[0]) * text_img.size[1]
		, WINDOW_H))

	px = 0 + w / 2 - ww / 2
	py = (wh + ABOVE_H) - ABOVE_H;

	window = Image.new('RGBA', (ww * 2, wh + ABOVE_H),
				(0,0,0,0))
	windraw = ImageDraw.Draw(window)
	windraw.polygon([(px, py), (px + ww / 2 - ABOVE_H, py),
			(px + ww / 2, wh + ABOVE_H),
			(px + ww / 2 + ABOVE_H, py),
			(px + ww, py), (px + ww, py - wh),
			(px, py - wh), (px, py)],
			fill=(255,255,255,192))
			#fill=(0,192,255,192))
	woff = (x, y - wh - ABOVE_H)

	img.paste(window, woff, mask=window)

	# ATTENTION! The value 1.2 here is a compensatory value for the
	# too small size of the word in the label picture
	r = max(text_img.size[0] / float(ww), text_img.size[1] / float(wh))
	rw = text_img.size[0] / r
	rh = text_img.size[1] / r
	attr_img = text_img.resize((int(rw * 1.2), int(rh * 1.2)))

	# So as the value 0.6 (0.6 = 1.2 / 2)
	img.paste(attr_img, (int(x + px + ww * 0.5 - rw * 0.6),
			     int(y - wh - ABOVE_H + wh * 0.5 - rh * 0.6)),
			     mask=attr_img)

	return img


def draw_box(img, result):
	img_w, img_h = img.size
	bg = Image.new('RGBA', (int(img_w + max(WINDOW_W, img_w * 0.1)),
				int(img_h + max(WINDOW_H * 2, img_h * 0.2))),
			(255,255,255,255))
	bg_w, bg_h = bg.size
	offset = ((bg_w - img_w) / 2, int((bg_h - img_h) / 2))
	bg.paste(img, offset)
	img = bg
	offset = {'x': offset[0], 'y': offset[1]}

	draw = ImageDraw.Draw(img)

	for i in range(0, len(result)):
		text_fn = classifier.classify(result[i])
		img = draw_single_box(img, draw, result[i]['boundingbox'],
					offset, Image.open(text_fn))
	return img
