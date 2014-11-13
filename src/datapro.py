# -*- coding: utf-8 -*-
import os
import sys
sys.path.append("..")
import re
import pickle
class WCharPro(object):
	"""docstring for WCharPro"""
	def __init__(self, wcdictfile, wcdictdata):
		self.wcdictfile = wcdictfile
		self.wcdictdata = wcdictdata
		self.wc2pydict = {}

		self.getWC2PYDict()
		self.saveWC2PYDict()
	
	def getWC2PYDict(self):
		try:
			pagedatalist = open(self.wcdictfile, 'r', encoding='utf_8_sig').readlines()
		except Exception:
			print('cannot open dict file !')
			exit()
		for linedata in pagedatalist:
			data = linedata[:-1]
			worddata = data[0]
			pinyinstr = data[1:]
			pattern = re.compile(r'[a-z]+')
			pinyindata = pattern.findall(pinyinstr)
			tempset = set(pinyindata)
			pinyindata = list(tempset)
			self.wc2pydict[worddata] = pinyindata

	def saveWC2PYDict(self):
		wcdictdata = open(self.wcdictdata,'wb')
		pickle.dump(self.wc2pydict,wcdictdata)
		wcdictdata.close()

class WStrPro(object):
	"""docstring for WStrPro"""
	def __init__(self, wsdictfile,py2wsdictdata):
		self.wsdictfile = wsdictfile
		self.py2wsdictdata = py2wsdictdata

		self.py2wsdict = {}
		self.getpy2wsdict()
		self.savepy2wsdict()

	def getpy2wsdict(self):
		try:
			pagedatalist = open(self.wsdictfile , 'r', encoding='utf_8_sig').readlines()
		except Exception:
			print('can not open dictfile file ')
			exit()
		for linedata in pagedatalist:
			data = linedata[:-1]
			pattern = re.compile(r'[a-z]')
			match = pattern.search(data)
			if match:
				index = data.index(match.group())
				word =  data[0:index-1]
				pinyinstr = data[index:]
				pattern = re.compile(r'[a-z]+')
				pinyindata = pattern.findall(pinyinstr)
				pinyin = ''.join(pinyindata)
				chindex = pinyin[0]
				if not chindex in self.py2wsdict.keys():
					self.py2wsdict[chindex] = {}
				tempworddict = self.py2wsdict[chindex]
				if pinyin in tempworddict:
					pinyinlist = tempworddict[pinyin]
					pinyinlist.append(word)
					pinyinlist = list(set(pinyinlist))
				else:
					pinyinlist = []
					pinyinlist.append(word)
				tempworddict[pinyin] = pinyinlist

	def savepy2wsdict(self):
		py2wsdictdata = open(self.py2wsdictdata , 'wb' )
		pickle.dump(self.py2wsdict,py2wsdictdata)
		py2wsdictdata.close()

class TrieTreePro(object):
	"""docstring for TrieTreePro"""
	def __init__(self, wsdictdata, triestorge):
		self.wsdictdata = wsdictdata
		self.triestorge = triestorge
		self.triedata = {}
		self.getTrieData()

	def createTrieTree(self,py2wsdict):
		for key in py2wsdict.keys():
			pt = self.triedata
			for ch in key:
				if not ch in pt:
					pt[ch] = {}
				pt = pt[ch]
			if key != '':
				if '#' in pt:
					tempdata = pt['#']
					datalist = tempdata.append(py2wsdict[key])
				else:
					datalist = list(py2wsdict[key])
				pt['#'] = datalist

	def getTrieData(self):
		try:
			pywdictdata = open(self.wsdictdata,'rb')
		except Exception:
			print('can not open datafile!!! ')
			exit()
		py2wsdict = pickle.load(pywdictdata)
		pywdictdata.close()
		for indexch in py2wsdict.keys():
			self.createTrieTree(py2wsdict[indexch])

			treefile = self.triestorge + indexch
			trietree = open(treefile , 'wb' )
			pickle.dump(self.triedata,trietree)
			trietree.close()
			self.triedata = {}

wcdictfile = r'./data/dict/wordchardict.txt'
wcdictdata = r'./data/wcdictdata'
if not os.path.exists(wcdictdata):
	wc = WCharPro(wcdictfile,wcdictdata)
wsdictfile = r'./data/dict/wordstrdict.txt'
wsdictdata = r'./data/wsdictdata'
if not os.path.exists(wsdictdata):
	ws = WStrPro(wsdictfile,wsdictdata)

triestorge = r'./data/trietrees/'
if not os.path.exists(triestorge):
	os.mkdir(triestorge)
	ttp = TrieTreePro(wsdictdata, triestorge)


