# Name:
# Date:
# Description:
#
#

import math, os, pickle, re

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
      for fFileObj in os.walk('movies_reviews/'):
         FileList = fFileObj[2]
         break
      for fileName in FileList:
         reviewText = self.loadFile('movies_reviews/' + fileName)
         reviewTokens = self.tokenize(reviewText)
         if 'movies-1' in fileName:
            for token in reviewTokens:
               if token in self.negativeDict:
                  self.negativeDict[token] += 1
               else:
                  negativeDict[token] = 1
         elif 'movies-5' in fileName:
            for token in reviewTokens:
               if token in self.positiveDict:
                  self.positiveDict[token] += 1
               else:
                  self.positiveDict[token] = 1
      self.save(self.negativeDict, 'negative_dictionary.txt')
      self.save(self.positiveDict, 'positive_dictionary.txt')


   def classify(self, sText):
      """Given a target string sText, this function returns the most likely document
      class to which the target string belongs (i.e., positive, negative or neutral).
      """
      words = self.tokenize(sText)
      ppos = 1.0
      pneg = 1.0

      poswords = float(sum(self.positiveDict.itervalues()))
      negwords = float(sum(self.negativeDict.itervalues()))
      totwords = poswords + negwords

      for word in words:
         pos = self.positiveDict.get( word, 0.0 ) + 1.0
         neg = self.negativeDict.get( word, 0.0 ) + 1.0
         totes = pos + neg

         ppos += math.log( (pos/poswords)/(poswords/totwords) )
         pneg += math.log( (neg/negwords)/(negwords/totwords) )

      # ptot = ppos + pneg

      print ppos
      print pneg

      if ppos == pneg:
         return "neutral"
      elif ppos > pneg:
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
