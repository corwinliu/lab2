import re

def mread_init():
	mread_fn = -1
	mread.it = 0
	mread.buffer = []

def mread(fn):
	if mread.fn != fn or (mread.it >= len(mread.buffer)):
		mread.buffer = re.split(' |\n|\r', fn.read())
		mread.it = 0
		mread.fn = fn

	while True:
		while mread.it < len(mread.buffer) and len(mread.buffer[mread.it]) == 0:
			mread.it += 1
		if mread.it == len(mread.buffer):
			mread.buffer = re.split(' |\n|\r', fn.read())
			mread.it = 0
			continue
		mread.it += 1
		return mread.buffer[mread.it - 1]

mread.fn = -1

def outname(fn, sfx):
	return ".".join(fn.split('.')[:-1]) + "_out." + sfx
