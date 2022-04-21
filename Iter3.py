
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
        self.greenLtrs=[]
        self.yellowLtrs=[]
        print("Starting with: " + str(len(self.words)) + " possible words")
        self.prob.addVariable("w",self.words)
        # self.prob.addConstraint(lambda x: x in self.words,"w")
        # self.prob.addConstraint(lambda x: x[0]=='a',"w")
        # x=self.prob.getSolutions()
        # self.prob.addConstraint(lambda x: x[1]=='b',"w")
        # x=self.prob.getSolutions()
        #print(x)

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
        #this iteration should only add black letter constraints for the 1st and 2nd guess, then for the 3rd guess we implement all constraints
        #this should give us the most optimally culled guess pool
        #still need a heuristic to pickaf
        #adding in constraints based on feedback from game
        #for some reason this needed to be hard coded for now, looping doesn't work too well
        g1=guess[0]
        g2=guess[1]
        g3=guess[2]
        g4=guess[3]
        g5=guess[4]
        s1=solution[0]
        s2=solution[1]
        s3=solution[2]
        s4=solution[3]
        s5=solution[4]
        self.prob.addConstraint(lambda x: x!=guess,"w")
        #if statements are "green" feedback, so letter is in the right spot
        #elif statements are "yellow" feedback, so letter is somewhere in the word
        #else statements are "black" feedback, so letter is not in the word
        if count<2:
            if( g1== s1 ):
                self.greenLtrs.append(g1)
                self.greenLtrIndex.append( (g1,0) )
            elif(g1 in solution):
                self.yellowLtrs.append(g1)
            else: 
                self.prob.addConstraint(lambda x: g1 not in x, "w")
            if( g2== s2 ):
                self.greenLtrs.append(g2)
                self.greenLtrIndex.append( (g2,1) )
            elif(g2 in solution):
                self.yellowLtrs.append(g2)
            else: 
                self.prob.addConstraint(lambda x: g2 not in x, "w")
            if( g3== s3 ):
                self.greenLtrs.append(g3)
                self.greenLtrIndex.append( (g3,2) )
            elif(g3 in solution):
                self.yellowLtrs.append(g3)
            else: 
                self.prob.addConstraint(lambda x: g3 not in x, "w")
            if( g4== s4 ):
                self.greenLtrs.append(g4)
                self.greenLtrIndex.append( (g4,3) )
            elif(g4 in solution):
                self.yellowLtrs.append(g4)
            else: 
                self.prob.addConstraint(lambda x: g4 not in x, "w")
            if( g5== s5 ):
                self.greenLtrs.append(g5)
                self.greenLtrIndex.append( (g5,4) )
            elif(g5 in solution):
                self.yellowLtrs.append(g5)
            else: 
                self.prob.addConstraint(lambda x: g5 not in x, "w")
        else:
            #add previously found green and yellow ltr constraints:
            if(count==2):
                print("adding in previously found constraints")
                for tup in self.greenLtrIndex:
                    self.prob.addConstraint(lambda x, l=tup: x[l[1]]==l[0],"w")
                for ltr in self.yellowLtrs:
                    self.prob.addConstraint(lambda x,l = ltr: l in x, "w")
                self.prob.addConstraint(lambda x: x in self.solutions,"w")
                #add in any new found constraints
            if( g1== s1 ):
                self.greenLtrs.append(g1)
                self.prob.addConstraint(lambda x: x[0]==g1, "w")
            elif(g1 in solution):
                self.yellowLtrs.append(g1)
                self.prob.addConstraint(lambda x : g1 in x, "w")
            else: 
                self.prob.addConstraint(lambda x: g1 not in x, "w")
            if( g2== s2 ):
                self.greenLtrs.append(g2)
                self.prob.addConstraint(lambda x: x[1]==g2, "w")
            elif(g2 in solution):
                self.yellowLtrs.append(g2)
                self.prob.addConstraint(lambda x : g2 in x, "w")
            else: 
                self.prob.addConstraint(lambda x: g2 not in x, "w")
            if( g3== s3 ):
                self.greenLtrs.append(g3)
                self.prob.addConstraint(lambda x: x[2]==g3, "w")
            elif(g3 in solution):
                self.yellowLtrs.append(g3)
                self.prob.addConstraint(lambda x : g3 in x, "w")
            else: 
                self.prob.addConstraint(lambda x: g3 not in x, "w")
            if( g4== s4 ):
                self.greenLtrs.append(g4)
                self.prob.addConstraint(lambda x: x[3]==g4, "w")
            elif(g4 in solution):
                self.yellowLtrs.append(g4)
                self.prob.addConstraint(lambda x : g4 in x, "w")
            else: 
                self.prob.addConstraint(lambda x: g4 not in x, "w")
            if( g5== s5 ):
                self.greenLtrs.append(g5)
                self.prob.addConstraint(lambda x: x[4]==g5, "w")
            elif(g5 in solution):
                self.yellowLtrs.append(g5)
                self.prob.addConstraint(lambda x : g5 in x, "w")
            else: 
                self.prob.addConstraint(lambda x: g5 not in x, "w")

    #read solution output into list
    #this elimates words from the possible list of guesses
    def parseOutput(self,input,guess):
        newPool=[]
        for tup in input:
            if(tup["w"]!=guess):
                newPool.append(tup["w"])
        return newPool

    def makeGuess(self,pool):
        maxScore=0
        curGuess=""
        for word in pool:
            curScore=0
            #check words score against current words score(herusitic) and pick the max of the two
            for ltr in word:
                if ltr not in self.greenLtrs:
                    curScore+=1
                if ltr not in self.yellowLtrs:
                    curScore+=1
                if self.countLtr(word,ltr)==1:
                    curScore+=1
                if ltr in self.vowels:
                    curScore+=1
            if curScore>maxScore:
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
        guess="crane"
        while(1):
            count+=1
            if(count!=1):
                guess=self.makeGuess(pool)
            print("Guessing : " + guess)
            if(guess!=solution):
                
                self.getFeedback(guess,solution,count)
                sols= self.prob.getSolutions()
                pool = self.parseOutput(sols,guess)
                print("Left with: " + str(len(pool)) + " possible choices.")
                #guess=random.choice(pool)

            else:
                print("Found answer in: " + str(count) + " tries.")
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
    print(freqs)
    goal=random.choice(solutions)
    response = input("Run Wordle Algorithm?\nType A if you want to see an average guess # over 100 tries\nType Q to run over all possible solutions (warning takes awhile)\nType Y/N to run once/cancel")
    if(response == "Y" or response =="y"):
        print("Running wordle algorithm")
        init=Wordle(words,solutions,goal,freqs)
        init.playGameAlg()
    elif(response =="A" or response =="a"):
        total=0
        for i in range(100):
            init=Wordle(words,solutions,goal,freqs)
            total+=init.playGameAlg()
        print("average # of guesses is: " + str(total/100))
    else:
        return None

if __name__=="__main__":
    main()