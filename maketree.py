#!/usr/bin/env python
#coding=utf-8
import string

#generate tree from treeseed
def gen_disease_tree():
	treeseed = open('data/treeseed_disease.txt','rU')
	treefile = open('data/treefile_disease.txt','w')

	for line in treeseed:
		# get low bound tree leaf
		title = '' 
		temp = line.split(';')
		#separate special value
		if temp[0][0] != 'E' and temp[0][0] != 'V':
			now = string.atoi(temp[0])
			bottom = string.atoi(temp[1].split(',')[0])
			top = string.atoi(temp[1].split(',')[1])
			if now > bottom:
				treefile.write(line)
				continue	
			index = line.find(';')
			while bottom <= top:
				stemp = str(bottom)
				if bottom < 100 and bottom >= 0:
					stemp = '0' + stemp
				if bottom < 10 and bottom >= 0:
					stemp = '0' + stemp
				treefile.write(stemp + line[index:])
				bottom = bottom + 1
		else:
			title = temp[0][0]
			now = string.atoi(temp[0][1:])
			bottom = string.atoi(temp[1].split(',')[0][1:])
			top = string.atoi(temp[1].split(',')[1][1:])
			if now > bottom:
				treefile.write(line)
				continue	
			index = line.find(';')
			while bottom <= top:
				stemp = str(bottom)
				if bottom < 10:
					stemp = '0' + stemp
				treefile.write(title + stemp + line[index:])
				bottom = bottom + 1
	treeseed.close()
	treefile.close()


def gen_income_tree():



if __name__ == '__main__':
	