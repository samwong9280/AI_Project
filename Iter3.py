
from pkg_resources import ContextualVersionConflict
import constraint
from constraint import *
import random

class Wordle():
    def __init__(self,words,solutions,goal,freqs):
        self.prob = Problem()
        self.vowels=['a','e','i','o','u']
        self.solutions=solutions
        self.words=words
        self.goal=goal
        self.freqs=freqs
        self.greenLtrIndex=[]
        self.yellowLtrsIndex=[]
        self.greenLtrs=[]
        self.yellowLtrs=[]
        print("Starting with: " + str(len(self.words)) + " possible words")
        self.prob.addVariable("w",self.words)

    #Testing function, allows player to guess, not intended for anything useful at the moment 
    def playGame(self):
        solution=random.choice(self.solutions)
        while(1):
            x=input("Guess a word\n")
            if(x in self.words):
                guess=x
            else:
                guess=None
                print("Not a word!")
                continue
            if(guess==solution):
                print("You got it!")
            else:
                print("Incorrect Guess!")
    
    def getFeedback(self,guess,solution,count):
        self.prob.addConstraint(lambda x: x!=guess,"w")
        self.prob.addConstraint(lambda x: x in self.solutions,"w")
        if count==2:
            print("adding in previously found constraints")
            for tup in self.greenLtrIndex:
                self.prob.addConstraint(lambda x, l=tup: x[l[1]]==l[0],"w")
            for tup in self.yellowLtrsIndex:
                self.prob.addConstraint(lambda x,l =tup[0]: l in x, "w")
                self.prob.addConstraint(lambda x,l=tup[0],n=tup[1]:x[n]!=l,"w")

        for i in range(len(guess)):
            #don't add in constraints yet so we have more freedom guessing second word
            if( count<2):
                if guess[i]==solution[i]:
                    self.greenLtrs.append(guess[i])
                    self.greenLtrIndex.append( (guess[i],i))
                elif guess[i] in solution:
                    self.yellowLtrs.append(guess[i])
                    self.yellowLtrsIndex.append( (guess[i],i))
                else:
                    self.prob.addConstraint(lambda x,l=guess[i]: l not in x,"w")
            #after second guess add in all constraints
            else:    
                if guess[i] == solution[i]:
                    self.prob.addConstraint(lambda x,l=guess[i],n=i: x[n]==l,"w")
                    self.greenLtrs.append(guess[i])
                elif guess[i] in solution:
                    self.prob.addConstraint(lambda x,l=guess[i]: l in x, "w")
                    self.prob.addConstraint(lambda x,l=guess[i],n=i: x[n]!=l,"w")
                    self.yellowLtrs.append(guess[i])
                else:
                    self.prob.addConstraint(lambda x,l=guess[i]: l not in x,"w")

    #read solution output into list
    #this elimates words from the possible list of guesses
    def parseOutput(self,input,guess):
        newPool=[]
        for tup in input:
            if(tup["w"]!=guess):
                newPool.append(tup["w"])
        return newPool

    def makeGuess(self,pool,count):
        maxScore=999
        curGuess=""
        # for word in pool:
        #     curScore=0
        #     #check words score against current words score(herusitic) and pick the max of the two
        #     for ltr in word:
        #         if ltr not in self.greenLtrs:
        #             curScore+=1
        #         if ltr not in self.yellowLtrs:
        #             curScore+=1
        #         if self.countLtr(word,ltr)==1:
        #             curScore+=1
        #         if ltr in self.vowels:
        #             curScore+=1
        #     if curScore>maxScore:
        #         maxScore=curScore
        #         curGuess=word
        if count <3:
            for word in pool:
                curScore = 0
                for i in range(len(word)):
                    curScore += self.freqs[word[i]][i]
                    if self.countLtr(word,word[i])>1:
                        curScore+=4-count
                if(curScore<maxScore):
                    maxScore=curScore
                    curGuess=word
        else:
            maxScore=0
            for word in pool:
                curScore = 0
                for i in range(len(word)):
                    curScore += self.freqs[word[i]][i]
                    if self.countLtr(word,word[i])>1:
                        curScore-=4-count
                if(curScore>maxScore):
                    maxScore=curScore
                    curGuess=word
        return curGuess
    
    def countLtr(self,w,l):
        count=0
        for ltr in w:
            if ltr==l:
                count+=1
        return count

    #simulate playing wordle
    def playGameAlg(self):
        solution=self.goal
        print("Trying to guess: " + solution)
        pool= self.words
        count=0
        guess="salet"
        while(1):
            count+=1
            if(count!=1):
                guess=self.makeGuess(pool,count)
            print("Guessing : " + guess)
            if(guess!=solution):
                
                self.getFeedback(guess,solution,count)
                sols= self.prob.getSolutions()
                pool = self.parseOutput(sols,guess)
                print("Left with: " + str(len(pool)) + " possible choices.")
                #guess=random.choice(pool)

            else:
                print("Found answer in: " + str(count) + " tries.\n")
                break
        return count
    
def genWords(solutions):
    #read in list of english words
    words=[]
    wordFile = open("english_words.txt")
    data = wordFile.readlines()
    print("imported " + str(len(data)) + " words from english_words.txt")
    wordFile.close()

    #store all of these stripped words of length 5 in an array
    for word in data:
        x=word.strip()
        if(len(x)==5):
            words.append(x)
    for word in solutions:
        if word not in words:
            words.append(word)
    print(str(len(words)) + " remain after eliminating non-5 letter words")
    return words

    #read in all possible solutions
def genSolutions():
    solutions=[]
    answerFile = open("words.txt","r")
    data = answerFile.readlines()
    print("imported " + str(len(data)) + " words from input file")
    answerFile.close()

    #store all words in array, strip the newline characters off the end of them
    for word in data:
        solutions.append(word.strip())
    return solutions

def getFreqs(words):
    freqs={'a':[0,0,0,0,0],
    'b':[0,0,0,0,0],
    'c':[0,0,0,0,0],
    'd':[0,0,0,0,0],
    'e':[0,0,0,0,0],
    'f':[0,0,0,0,0],
    'g':[0,0,0,0,0],
    'h':[0,0,0,0,0],
    'i':[0,0,0,0,0],
    'j':[0,0,0,0,0],
    'k':[0,0,0,0,0],
    'l':[0,0,0,0,0],
    'm':[0,0,0,0,0],
    'n':[0,0,0,0,0],
    'o':[0,0,0,0,0],
    'p':[0,0,0,0,0],
    'q':[0,0,0,0,0],
    'r':[0,0,0,0,0],
    's':[0,0,0,0,0],
    't':[0,0,0,0,0],
    'u':[0,0,0,0,0],
    'v':[0,0,0,0,0],
    'w':[0,0,0,0,0],
    'x':[0,0,0,0,0],
    'y':[0,0,0,0,0],
    'z':[0,0,0,0,0]
    }
    #get frequencies store max and min
    for word in words:
        for i in range(len(word)):
            freqs[word[i]][i]+=1

    #get max and min
    vals=freqs.values()
    maxF=0
    minF=0
    for val in vals:
        maxF=max(maxF, max(val))
        minF=min(minF, min(val))
    
    #normalize
    for key in freqs:
        val = freqs[key]
        for i in range(len(val)):
            freqs[key][i]=normalize(freqs[key][i],minF,maxF)
    return freqs
    
def normalize(x, minX, maxX):
    return (x-minX)/(maxX-minX)

def main():
    solutions=genSolutions()
    words=genWords(solutions)
    freqs=getFreqs(words)
    goal=random.choice(solutions)
    response = input("Run Wordle Algorithm?\nType A if you want to see an average guess # over 100 tries\nType Q to run over all possible solutions (warning takes awhile)\nType Y/N to run once/cancel")
    if(response == "Y" or response =="y"):
        print("Running wordle algorithm")
        init=Wordle(words,solutions,"daunt",freqs)
        init.playGameAlg()
    elif(response =="A" or response =="a"):
        total=0
        for i in range(10):
            goal=random.choice(solutions)
            init=Wordle(words,solutions,goal,freqs)
            total+=init.playGameAlg()
        print("average # of guesses is: " + str(total/10))
    elif(response =="Q" or response =="q"):
        total=0
        for word in solutions:
            init =Wordle(words, solutions, word,freqs)
            total += init.playGameAlg()
        print("Average number of guesses over all solutions is: " +str(total/len(solutions)))
    else:
        return None

if __name__=="__main__":
    main()