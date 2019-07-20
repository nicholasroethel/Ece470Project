import nltk
import sklearn
import random
import copy
import math
import numpy as np
from nltk.corpus import words
from random import sample
from Config import get_config, print_usage

import string
import random

englishString = ""
nonenglishString = ""

def random_string(length):
  return convertToIntArray(''.join(random.choice(string.ascii_lowercase) for m in range(length)))

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

def evaluate(crib, item,encryptedMessage):
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
  
  return phiScore + hammingScore

def crossover(item1,item2):
  crossoverPoint = random.randint(0,len(item1))
  return np.append(item1[:crossoverPoint],item2[crossoverPoint:]), np.append(item2[:crossoverPoint],item1[crossoverPoint:])

def mutate(item):
  randChar = ord(random.choice(string.ascii_lowercase))
  position = random.randint(0,len(item)-1)
  item[position] = randChar
  
  return item

def convertToIntArray(item):
  return np.asarray([ord(c) for c in item])

def convertIntArrayToString(item):
  return ''.join([chr(i) for i in item])

def initPop(config):
  return np.asarray([random_string(config.key_len) for i in range(config.pop_size)])

def calcFitness(items,config,encryptedMessage):
  return np.asarray([evaluate(config.crib, item,encryptedMessage) for item in items])

def repeatKey(key, stringlen):
  n = stringlen/len(key)
  times = int(n+1)
  new = np.tile(key,times)
  return new[:stringlen]

def encodeString(key,string):
  string[string == 32] =123
  return ((string-97)+ (repeatKey(key,len(string))-97))%27 +97 

def decodeString(key, string):
  decodedString = ((string-97)-(repeatKey(key,len(string))-97))%27 +97
  decodedString[decodedString ==123] =32
  return decodedString

def loopLogic(key,config,initialMessage):
  
  encryptedMessage = encodeString(key,initialMessage.copy())

  maxFitnesses = []

  population = initPop(config)
  fitnesses = calcFitness(population,config,encryptedMessage)
  
  maxgen = config.max_gen

  for i in range(config.max_gen):
    #print("Gen Number = "+ str(i))
    parents = population[np.random.choice(len(fitnesses),int(len(fitnesses)* config.survival_rate),False,fitnesses/fitnesses.sum()),:]
    population = parents
    while len(population)<config.pop_size:
      child1,child2 = crossover(parents[np.random.choice(len(parents)),:],parents[np.random.choice(len(parents)),:])
      if random.random() < config.mutate_chance:
        child1 = mutate(child1)
      if random.random() < config.mutate_chance:
        child2 = mutate(child2)
      population = np.append(population,[child1,child2],0)
    #print("Max fitness:")
    fitnesses = calcFitness(population,config,encryptedMessage)
    maxFitnesses.append(fitnesses.max())
    #print(fitnesses.max())
    if i > config.convergence_number:
      if np.average(maxFitnesses[-1*config.convergence_number:]) == maxFitnesses[-1] and maxFitnesses[-1] > config.convergence_threshold:
        maxgen = i
        break
  print("The Best Key Found This Generation:")
  print(convertIntArrayToString(population[fitnesses.argmax()]))
  return maxgen

def calcGenerationsFitness(population,config,initialMessage):
  gens = []
  for key in population:
    gens.append(loopLogic(key,config,initialMessage))
  return np.asarray(gens)

def main(config):
  initialMessage = genRandom(config.crib,config.message_len)
  maxFitnesses = []
  population = initPop(config)
  fitnesses = calcGenerationsFitness(population, config, initialMessage)
  
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
    #print("Max fitness:")
    fitnesses = calcGenerationsFitness(population,config,initialMessage)
    maxFitnesses.append(fitnesses.max())
    #print(fitnesses.max())
    if i > config.convergence_number:
      if np.average(maxFitnesses[-1*config.convergence_number:]) == maxFitnesses[-1] and maxFitnesses[-1] > config.convergence_threshold:
        break
  print("The Overall Best Key Found:")
  print(convertIntArrayToString(population[fitnesses.argmax()]))


if __name__== "__main__":
  config, unparsed = get_config()
  # If we have unparsed arguments, print usage and exit
  if len(unparsed) > 0:
      print_usage()
      exit(1)
  nltk.download('words')
  main(config)