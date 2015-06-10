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
	wh = int(min(ww / float(text_img.size[0]) * text_img.size[1] * 2
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
			fill=(0,192,255,192))
	woff = (x, y - wh - ABOVE_H)

	img.paste(window, woff, mask=window)

	attr_img = text_img.resize((ww, wh))
	img.paste(attr_img, (x + px, y - wh - ABOVE_H), mask=attr_img)

	return img


def draw_box(img, result):
	img_w, img_h = img.size
	bg = Image.new('RGBA', (int(img_w + max(WINDOW_W * 2, img_w * 0.4)),
				int(img_h + max(WINDOW_W * 2, img_h * 0.4))),
			(0,128,255,255))
	bg_w, bg_h = bg.size
	offset = ((bg_w - img_w) / 2, (bg_h - img_h) / 2)
	bg.paste(img, offset)
	img = bg
	offset = {'x': (bg_w - img_w) / 2, 'y': (bg_h - img_h) / 2}

	draw = ImageDraw.Draw(img)

	for i in range(0, len(result)):
		text_fn = classifier.classify(result[i])
		img = draw_single_box(img, draw, result[i]['boundingbox'],
					offset, Image.open(text_fn))
	return img
