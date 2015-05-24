# Name:
# Date:
# Description:
#
#

import math, os, pickle, re, random

class Bayes_Classifier:

   def __init__(self):
      """This method initializes and trains the Naive Bayes Sentiment Classifier.  If a
      cache of a trained classifier has been stored, it loads this cache.  Otherwise,
      the system will proceed through training.  After running this method, the classifier
      is ready to classify input text."""
      self.positiveDict = {}
      self.negativeDict = {}
      if os.path.exists('positive_dictionary.txt'):
         self.positiveDict = self.load('positive_dictionary.txt')
         self.negativeDict = self.load('negative_dictionary.txt')
      else:
         self.train()


   def train(self):
      """Trains the Naive Bayes Sentiment Classifier."""
      FileList = []
      good = 0
      bad = 0
      for fFileObj in os.walk('movies_reviews/'):
         FileList = fFileObj[2]
         break
      for fileName in FileList:
         reviewText = self.loadFile('movies_reviews/' + fileName)
         reviewTokens = self.tokenize(reviewText)
         if 'movies-1' in fileName:
            good += 1
            for token in reviewTokens:
               if token in self.negativeDict:
                  self.negativeDict[token] += 1
               else:
                  negativeDict[token] = 1
         elif 'movies-5' in fileName:
            bad += 1
            for token in reviewTokens:
               if token in self.positiveDict:
                  self.positiveDict[token] += 1
               else:
                  self.positiveDict[token] = 1
      # print "There are ", good, " good reviews and ", bad, " bad reviews"
      self.save(self.negativeDict, 'negative_dictionary.txt')
      self.save(self.positiveDict, 'positive_dictionary.txt')

   def evaluate(self):
      FileList = []
      TenFold = [[] for i in range(10)]
      for fFileObj in os.walk('movies_reviews/'):
         FileList = fFileObj[2]
         break
      random.shuffle(FileList)

      for fileName in FileList:

         r = random.uniform(0,10)
         TenFold[int(r)].append(fileName)

      posPrecision = 0
      posRecall = 0
      negPrecision = 0
      negRecall = 0
      posFmeasure = 0
      negFmeasure = 0
      for i in range(10):
         testData = TenFold[i]
         trainingData = []
         for j in range(10):
            if i == j:
               continue
            trainingData = list(set(trainingData) | set(TenFold[j]))
         self.tPositiveDict = {}
         self.tNegativeDict = {}

         for fileName in trainingData:
            reviewText = self.loadFile('movies_reviews/' + fileName)
            reviewTokens = self.tokenize(reviewText)
            if 'movies-1' in fileName:
               for token in reviewTokens:
                  if token in self.tNegativeDict:
                     self.tNegativeDict[token] += 1
                  else:
                     self.tNegativeDict[token] = 1
            elif 'movies-5' in fileName:
               for token in reviewTokens:
                  if token in self.tPositiveDict:
                     self.tPositiveDict[token] += 1
                  else:
                     self.tPositiveDict[token] = 1
         posCorrect = 0
         negCorrect = 0
         posWrong = 0
         negWrong = 0
         for instance in testData:
            instanceText = self.loadFile('movies_reviews/' + instance)
            if(self.classify(instanceText) == 'positive'):
               if 'movies-5' in instance:
                  posCorrect += 1
               else:
                  posWrong += 1
            if(self.classify(instanceText) == 'negative'):
               if 'movies-1' in instance:
                  negCorrect += 1
               else:
                  negWrong += 1
         PP = float(posCorrect) / (float(posCorrect) + float(posWrong))
         PR = float(posCorrect) / (float(posCorrect) + float(negWrong))
         NP = float(negCorrect) / (float(negCorrect) + float(negWrong))
         NR = float(negCorrect) / (float(negCorrect) + float(posWrong))
         PFM = 2 * PP * PR /(PP + PR)
         NFM = 2 * NP * NR / (NP +NR)

         posPrecision += PP
         posRecall += PR
         negPrecision += NP
         negRecall += NR
         posFmeasure += PFM
         negFmeasure += NFM
         print "==================TEST RUN ", i, "==============="
         print "positive precision: ", PP, " positive recall: ", PR, " negative precision: ", NP, " negative recall: ", NR, " negative F measure: ", NFM, " positive F measure: ", PFM

      posPrecision /= 10
      posRecall /= 10
      negPrecision /= 10
      negRecall /= 10
      negFmeasure /= 10
      posFmeasure /= 10
      print "\n FINAL RESULTS"
      print "positive precision: ", posPrecision, " positive recall: ", posRecall, " negative precision: ", negPrecision, " negative recall: ", negRecall, " negative F measure: ", negFmeasure, " positive F measure: ", posFmeasure



   def classify(self, sText, tenFold = False):
      """Given a target string sText, this function returns the most likely document
      class to which the target string belongs (i.e., positive, negative or neutral).
      """
      if tenFold == False:
         posDict = self.positiveDict
         negDict = self.negativeDict
      else:
         posDict = self.tPositiveDict
         negDict = self.tNegativeDict


      words = self.tokenize(sText)
      ppos = 1.0
      pneg = 1.0

      poswords = float(sum(posDict.itervalues()))
      negwords = float(sum(negDict.itervalues()))
      totwords = poswords + negwords


      for word in words:
         pos = posDict.get( word, 0.0 ) + 1.0
         neg = negDict.get( word, 0.0 ) + 1.0

         # print "It occurs ", pos, " in positive reviews and ", neg, "  times in negative reviews"
         ppos += math.log( pos/(poswords/totwords) )
         pneg += math.log( neg/(negwords/totwords) )

      # ptot = ppos + pneg

      # print "Positive: ", ppos
      # print "Negative: ", pneg


      if ppos >= pneg:
         return "positive"
      else: # pneg > ppos
         return "negative"


   def loadFile(self, sFilename):
      """Given a file name, return the contents of the file as a string."""

      f = open(sFilename, "r")
      sTxt = f.read()
      f.close()
      return sTxt

   def save(self, dObj, sFilename):
      """Given an object and a file name, write the object to the file using pickle."""

      f = open(sFilename, "w")
      p = pickle.Pickler(f)
      p.dump(dObj)
      f.close()

   def load(self, sFilename):
      """Given a file name, load and return the object stored in the file."""

      f = open(sFilename, "r")
      u = pickle.Unpickler(f)
      dObj = u.load()
      f.close()
      return dObj

   def tokenize(self, sText):
      """Given a string of text sText, returns a list of the individual tokens that
      occur in that string (in order)."""

      lTokens = []
      sToken = ""
      for c in sText:
         if re.match("[a-zA-Z0-9]", str(c)) != None or c == "\"" or c == "_" or c == "-":
            sToken += c
         else:
            if sToken != "":
               lTokens.append(sToken)
               sToken = ""
            if c.strip() != "":
               lTokens.append(str(c.strip()))

      if sToken != "":
         lTokens.append(sToken)

      return lTokens


def t():
   b = Bayes_Classifier()
   print "poo tities balls bears bad horrible:\n"
   print b.classify("poo tities balls bears bad horrible")
   print "\nawesome great terrific praise amazing:\n"
   print b.classify("awesome great terrific praise amazing\n")

def test(string):
   b = Bayes_Classifier()
   print string, ' was rated \n', b.classify(string)
