import nltk
import random
import numpy as np
from nltk.corpus import words
from random import sample

import string
import random
def random_string(length):
    return ''.join(random.choice(string.ascii_letters) for m in range(length))

def genRandom(n):
	randString = ' '.join(sample(words.words(), n))
	return randString

def evaluate(item):
    item1 = genRandom(6)
    item2 = genRandom(6)
    item3 = random_string(40)
    item1 = [ord(c) for c in item1][:40]
    item2 = [ord(c) for c in item2][:40]
    item3 = [ord(c) for c in item3]

    realcor = np.corrcoef(item1,item2)[0][1]
    fakecor = np.corrcoef(item1,item3)[0][1]
    if(realcor > fakecor):
        return 1
    else:
        return 0

def main():
    nltk.download('words')
    sum = 0
    for i in range(100):
        sum += evaluate(None)
    print(sum/100)
  
if __name__== "__main__":
  main()