import sys
from lxml import html
import requests

#clue = str(sys.argv[1])
#length = int(sys.argv[2])

#clue = ""
#count = 1
#for i in range(1,len(sys.argv)-2):
#	clue+=sys.argv[i]+"+"
#clue+=sys.argv[len(sys.argv)-2]
#length = int(sys.argv[len(sys.argv)-1])

def solveClue(clue,length):
	patternTag = '%3F'*length
	link = 'http://www.dictionary.com/fun/crosswordsolver?query='+clue+'&pattern='+patternTag+'&l='+str(length)

	page = requests.get(link)
	tree = html.fromstring(page.content)

	answerList = tree.xpath('//div[@class="matching-answer"]/text()')

	answers = []
	for answer in answerList:
		answers.append(answer.strip())
	if len(answers)!=0:
		answers.remove('Matching Answer')
		return answers
	else:
		return False

print(solveClue("foodxcxvxcv",8))