import src.datapro
import src.wpyfix as wpyfix

testinput = '夏雨'
fw = wpyfix.FixWord(testinput)
print('input word', testinput)
print('suggest words', fw.word)