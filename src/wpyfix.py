# -*- coding: utf-8 -*-
import sys
sys.path.append("..")
import re
import pickle

class WS2PY(object):
	"""docstring for WPYFix"""
	def __init__(self,inputstr):
		self.inputstr = inputstr
		self.wcdictdata = r'./data/wcdictdata'
		self.wc2pydict = self.getWC2PYDict(self.wcdictdata)
		self.wc2pylist = []
		self.resultlist = []
		self.execute(self.inputstr)

	def getWC2PYDict(self,wcdictdata):
		try:
			pywdictdata = open(wcdictdata,'rb')
		except Exception:
			print('can not open wcdictdata datafile!!! ')
			exit()
		wc2pydict = pickle.load(pywdictdata)
		pywdictdata.close()
		return wc2pydict

	def getW2PYList(self):
		for word in self.inputstr:
			self.wc2pylist.append(self.wc2pydict[word])

	def getfixpylist(self):
		row = len(self.wc2pylist)
		lenlist = []
		for index in range(0,row):
			lenlist.append(len(self.wc2pylist[index]))
		col = max(lenlist)
		propath=[]	
		self.choiceCombe(row,col,0,[],propath)	
		for item in propath:
			tempstr = ''
			for x in range(0,len(item)):
				numdata = item[x]
				if numdata > lenlist[x]-1:
					tempstr = ''
					break
				else:
					tempstr = tempstr + self.wc2pylist[x][numdata] + '#'
			if tempstr:
				self.resultlist.append(tempstr)

	def choiceCombe(self,depth,length,index,templist,outlist):
		if index >= depth:
			outlist.append(templist)
			return
		for x in range(0,length):
			self.choiceCombe(depth, length, index+1, templist+[x],outlist)
	
	def execute(self,testinput):
		self.getW2PYList()
		self.getfixpylist()

class PY2Word(object):
	"""docstring for PY2Word"""
	def __init__(self,pinyinlist):
		self.pinyinlist = pinyinlist
		self.storgepath = r'./data/trietrees/'
		self.trietree = {}
		self.worddata = []
		self.getWordList()

	def getWordList(self):
		for pinyin in self.pinyinlist:
			indexchar = pinyin[0]
			triefile = self.storgepath + indexchar
			self.getTrieTree(triefile)
			wordlist = self.getItem(pinyin)
			self.worddata.extend(wordlist)

	def getTrieTree(self,trietree):
		try:
			trietreedata = open(trietree,'rb')
		except Exception:
			print('can not open storgepath datafile!!! ')
			exit()
		self.trietree = pickle.load(trietreedata)
		trietreedata.close()

	def getItem(self,keyword):
		pt = self.trietree
		for ch in keyword:
			if not ch in pt:
				return []
			pt = pt[ch]
		if '#' in pt:
			worddata = pt['#']
			return worddata
		return []

class PYFIX(object):
	"""docstring for PYFIX"""
	def __init__(self,inputpy):
		# self.inputpy = inputpy
		self.pylist = inputpy.split('#')[:-1]
		self.patternlist = []
		self.dic = {'s':'sh','c':'ch','z':'zh',
				'sh':'s','ch':'c','zh':'z',
				'an':'ang','en':'eng','on':'ong','in':'ing',
				'ang':'an','eng':'en','ong':'on','ing':'in',
				'na':'la','ni':'li','ne':'le','nu':'lu',
				'l':'n'}
		self.initPattern()
		self.fixchlist = []
		self.replacedata = []
		self.pychoicelist = []
		self.fixpylist = []

		self.execute()
	
	def initPattern(self):
		patstrs = [r'[zcs](?!h)',r'[zcs]h',r'[aeo]ng',r'[aeo]n(?!g)',r'^n[aieu]',r'^l']
		for pats in patstrs:
			pattern = re.compile(pats)
			self.patternlist.append(pattern)

	def getFixcharList(self):
		for py in self.pylist:
			templist = []
			for pattern in self.patternlist:
				matchresults = pattern.findall(py)
				for data in matchresults:
					templist.append(data)	
			self.fixchlist.append(templist)		

	def getReplacedata(self):
		for fixch in self.fixchlist:
			listsize = len(fixch)
			templist = []
			for x in range(1,listsize+1):
				self.perm(listsize, x, 1, [],templist)
			self.replacedata.append(templist)

	def perm(self,totalsize, choicenum, currentindex, datalist,outlist):
		if choicenum == len(datalist):
			data = ''.join(datalist)
			outlist.append(data)
			return
		for x in range(currentindex,totalsize+1):
		 	if x not in datalist:
		 		self.perm(totalsize, choicenum, x+1, datalist + [str(x)],outlist)
		return

	def getPYchoiceList(self):
		pylength = len(self.pylist)
		for pyindex in range(0,pylength):
			rplength = len(self.replacedata[pyindex])
			repalcelist = [self.pylist[pyindex]]
			for rpindex in range(0,rplength):
				data = self.pylist[pyindex]
				for ch in self.replacedata[pyindex][rpindex]:
					replacemark = int(ch) -1
					oldchar = self.fixchlist[pyindex][replacemark]
					data = data.replace(oldchar,self.dic[oldchar])
				repalcelist.append(data)
			self.pychoicelist.append(repalcelist)

	def choiceCombe(self,depth,length,index,templist,outlist):
		if index >= depth:
			outlist.append(templist)
			return
		for x in range(0,length):
			self.choiceCombe(depth, length, index+1, templist+[x],outlist)

	def getFixpylist(self):
		depth = len(self.pychoicelist)
		lenlist=[]
		for index in range(0,depth):
			lenlist.append(len(self.pychoicelist[index]))
		if lenlist:
			length = max(lenlist)
		else:
			length =0
		# print('lenlist', lenlist)
		tempoutlist = []
		self.choiceCombe(depth, length, 0, [], tempoutlist)
		# print('tempoutlist', tempoutlist)
		for item in tempoutlist:
			tempstr = ''
			for x in range(0,len(item)):
				numdata = item[x]
				if numdata > lenlist[x] -1:
					tempstr = ''
					break
				else:
					tempstr = tempstr + self.pychoicelist[x][numdata]
			if tempstr:
				self.fixpylist.append(tempstr)

	def execute(self):
		self.getFixcharList()
		self.getReplacedata()
		self.getPYchoiceList()
		self.getFixpylist()

class FixWord(object):
	"""docstring for FixWord"""
	def __init__(self,inputword):
		self.inputword = inputword
		self.wordlength = len(inputword)
		self.wordlist = []
		self.worddict = {}
		self.word = []
		self.getWordList()
		self.getWordDict()
	
	def getWordList(self):
		wp = WS2PY(self.inputword)
		pylist = wp.resultlist
		fixpylist = []
		for pinyin in pylist:
			pyfix = PYFIX(pinyin)
			pydatalist = pyfix.fixpylist
			fixpylist.extend(pydatalist)
		pt2w = PY2Word(fixpylist)
		self.wordlist = pt2w.worddata
		
	def levenshtein(self,firststr,secondstr):
	    fststrlen = len(firststr)
	    sndstrlen = len(secondstr)
	    if fststrlen == 0:
	        return sndstrlen
	    if sndstrlen == 0:
	        return fststrlen
	    col = fststrlen + 1
	    row = sndstrlen + 1
	    distmatrix = [[0 for col in range(col)] for row in range(row)]
	    distmatrix[0] = list(range(0,col))
	    for x in range(0,row):
	        distmatrix[x][0] = x
	    
	    for rowindex in range(1,row):
	        for colindex in range(1,col):
	            deletion = distmatrix[rowindex-1][colindex] + 1
	            insertion = distmatrix[rowindex][colindex-1] + 1  
	            substitution = distmatrix[rowindex-1][colindex-1]
	            if firststr[colindex-1] != secondstr[rowindex-1]:
	                substitution += 1
	            distmatrix[rowindex][colindex] = min(insertion,deletion,substitution)    
	    return distmatrix[sndstrlen][fststrlen]  

	def getWordDict(self):
		for word in self.wordlist:
			dist = self.levenshtein(self.inputword,word)
			self.worddict[word] = dist
		worddict = self.worddict
		resultdict = sorted(worddict.items(),key= lambda worddict:worddict[1],reverse=False)
		for rowdata in resultdict:
			data = int(rowdata[1])
			if data <= 0.5*self.wordlength:
				self.word.append(rowdata[0])


# testinput = '男球'

# fw = FixWord(testinput)
# print(fw.word)


