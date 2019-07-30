import nltk
import sklearn
import random
import copy
import math
import numpy as np
from nltk.corpus import words
from random import sample
from Config import get_config, print_usage
import matplotlib.pyplot as plt

import string
import random

englishString = ""
nonenglishString = ""

#Generates a string of random charcters of fixed length
def random_string(length):
  return convertToIntArray(''.join(random.choice(string.ascii_lowercase) for m in range(length)))

#Generates a string of random english words of fixed length
def genRandom(crib,n):
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

	return convertToIntArray((crib + " " + randString).lower())

#Calculates fitness score for given item
def evaluate(config, crib, item, encryptedMessage):
  global englishString
  global nonenglishString
  if englishString == "":
    englishString = genRandom(crib,len(encryptedMessage)-len(crib)-1)
    nonenglishString = random_string(len(encryptedMessage))

  item1 = decodeString(item,encryptedMessage)
  cribArray = convertToIntArray(crib)

  realcor = sklearn.metrics.matthews_corrcoef(item1,englishString)
  fakecor = sklearn.metrics.matthews_corrcoef(item1,nonenglishString)

  phiScore = (abs(realcor) - abs(fakecor) + 1)/4
  hammingScore = np.sum(np.ones(len(crib))[cribArray==item1[:len(crib)]]) / (len(crib)*2)
  
  return np.power(phiScore + hammingScore,config.bias_exponent)

#Returns the 2 crossover products of the items passed in
def crossover(item1,item2):
  crossoverPoint = random.randint(0,len(item1))
  return np.append(item1[:crossoverPoint],item2[crossoverPoint:]), np.append(item2[:crossoverPoint],item1[crossoverPoint:])

#Returns a mutation of the item passed in
def mutate(item):
  randChar = ord(random.choice(string.ascii_lowercase))
  position = random.randint(0,len(item)-1)
  item[position] = randChar
  
  return item

#Converts string to int array of ascii value
def convertToIntArray(item):
  return np.asarray([ord(c) for c in item])

#Converts int array of ascii values to string
def convertIntArrayToString(item):
  return ''.join([chr(i) for i in item])

#returns a population of random strings
def initPop(config):
  return np.asarray([random_string(config.key_len) for i in range(config.pop_size)])

#generates an array of fitness scores for an array of given items
def calcFitness(items,config,encryptedMessage):
  return np.asarray([evaluate(config,config.crib, item,encryptedMessage) for item in items])

#helper function to tile key used for vignere encrytption
def repeatKey(key, stringlen):
  n = stringlen/len(key)
  times = int(n+1)
  new = np.tile(key,times)
  return new[:stringlen]

#encodes int array using a vignere cipher 
def encodeString(key,string):
  string[string == 32] =123
  return ((string-97)+ (repeatKey(key,len(string))-97))%27 +97 

#decodes an int array using a vignere cipher
def decodeString(key, string):
  decodedString = ((string-97)-(repeatKey(key,len(string))-97))%27 +97
  decodedString[decodedString ==123] =32
  return decodedString

#Runs GA with diffrent values for given parameter and generates graph based on the result
def main(config):
  values = [1,2,3,4,5] #Values to use for parameter testing
  resultsSuccess = []
  resultsGen = []
  for i in values:
    print(i)
    config.bias_exponen = i #Parameter to test
    tempSuccess = []
    tempGen = []
    for j in range(config.runs_per_value):
      success , gen = runGA(config)
      tempSuccess.append(success)
      tempGen.append(gen)
    print(np.average(tempSuccess))
    print(np.average(tempGen))
  
    resultsSuccess.append(np.average(tempSuccess))
    resultsGen.append(np.average(tempGen))
  figure, plt1 = plt.subplots()

  plt1.set_xlabel("Bias Factor")
  plt1.set_ylabel("Generations",color='tab:orange')
  plt1.plot(values,resultsGen,color='tab:orange')
  plt1.tick_params(axis="y",labelcolor='tab:orange')

  plt2 = plt1.twinx()
  plt2.set_ylabel("Success Rate",color='tab:blue')
  plt2.plot(values,resultsSuccess,color='tab:blue')
  plt2.tick_params(axis="y",labelcolor='tab:blue')

  figure.tight_layout()
  plt.title("Bias Factor")
  plt.show()


#Contains the actual GA code
def runGA(config):
  initialMessage = genRandom(config.crib,config.message_len)
  initialKey = random_string(config.key_len)
  encryptedMessage = encodeString(initialKey,initialMessage.copy())

  maxFitnesses = []

  population = initPop(config)
  fitnesses = calcFitness(population,config,encryptedMessage)
  
  endGen = config.max_gen
  for i in range(config.max_gen):
    parents = population[np.random.choice(len(fitnesses),int(len(fitnesses)* config.survival_rate),False,fitnesses/fitnesses.sum()),:]
    population = parents
    while len(population)<config.pop_size:
      child1,child2 = crossover(parents[np.random.choice(len(parents)),:],parents[np.random.choice(len(parents)),:])
      if random.random() < config.mutate_chance:
        child1 = mutate(child1)
      if random.random() < config.mutate_chance:
        child2 = mutate(child2)
      population = np.append(population,[child1,child2],0)
    fitnesses = calcFitness(population,config,encryptedMessage)
    maxFitnesses.append(fitnesses.max())
    if np.array_equal(population[fitnesses.argmax()],initialKey):
      endGen = i
      break
  return decodeString(population[fitnesses.argmax()],encryptedMessage) == initialMessage, endGen
  
if __name__== "__main__":
  config, unparsed = get_config()
  # If we have unparsed arguments, print usage and exit
  if len(unparsed) > 0:
      print_usage()
      exit(1)
  nltk.download('words')
  main(config)