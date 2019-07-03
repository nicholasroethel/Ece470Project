import nltk
import random
from nltk.corpus import words
from random import sample

def genRandom(n):
	randString = ' '.join(sample(words.words(), n))
	print(randString)

def main():
  nltk.download('words')
  n = 5
  genRandom(n)
  
if __name__== "__main__":
  main()