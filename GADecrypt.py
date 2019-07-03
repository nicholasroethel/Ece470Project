import nltk
import sklearn
import random
from nltk.corpus import words
from random import sample

import string
import random
def random_string(length):
    return ''.join(random.choice(string.ascii_letters) for m in range(length))

def genRandom(n):
	wordlist = words.words()
	randString = ''


	while len(randString) < n: #keeps adding to randstring until its length n
		#print(len(randString))

		if ((len(randString)<1)  or (len(randString) > n-3)): #gets first part or resets to speed up probability of finding proper string length
			randString =  ''
			while(len(randString)<1):
				tmpword = random.choice(wordlist)
				if len(tmpword) < n:
					randString = tmpword

		tmpword = random.choice(wordlist)
		tmplen = len(tmpword)

		if (len(randString) + 1 + tmplen)<=n: #add to the string if possible
			randString = randString + ' ' + tmpword 

	return randString

def evaluate(item):
    item1 = genRandom(40)
    item2 = genRandom(40)
    item3 = random_string(40)
    item1 = [ord(c) for c in item1]
    item2 = [ord(c) for c in item2]
    item3 = [ord(c) for c in item3]

    realcor = sklearn.metrics.matthews_corrcoef(item1,item2)
    fakecor = sklearn.metrics.matthews_corrcoef(item1,item3)
    if(abs(realcor) > abs(fakecor)):
        return 1
    else:
        return 0

def main():
    nltk.download('words')
    n = 50
    randString = genRandom(n)
    print(randString)
    sum = 0
    for i in range(100):
    	sum += evaluate(None)
    print(sum/100)
  
if __name__== "__main__":
  main()