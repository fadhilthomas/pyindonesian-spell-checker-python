import enchant
import sys
import re
from collections import Counter as mset
from argparse import ArgumentParser

def check(arr, string):
	out = []
	for i in arr:
		if len(list((mset(i) & mset(string)).elements())) == len(string):
			out.append(i)
	if len(out) == 0:
		out = arr
	return out[0]

def load():
	d = {}
	with open("train.txt") as f:
		for line in f:
			(key, val) = line.split()
			d[key] = val
	return d

def sanitize(s):
	s = re.sub(r'[^\w]', ' ', s)
	s = " ".join(s.split())
	s = s.strip()
	return s

def main():
	argp = ArgumentParser(usage="python spell_check.py [-i text ]")
	argp.add_argument('-i', dest='input', required=True, help='Input text')
	args = argp.parse_args()
	input_str = sanitize(args.input)
	output_str = []
	dict = enchant.PyPWL("KBBI.txt")
	d = load()
	arr_str = input_str.split(' ')
	for i in arr_str:
		if dict.check(i) == True:
			output_str.append(i)
		else:
			if i in d:
				output_str.append(d.get(i))
			else:
				output_str.append(check(dict.suggest(i), i))

	print ' '.join(output_str)

if __name__ == "__main__":
	main()