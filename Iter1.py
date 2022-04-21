
import constraint
from constraint import *
import random



class Wordle():
    def __init__(self,words,solutions,goal):
        self.prob = Problem()
        #self.domain = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
        #self.prob.addVariables(["x1","x2","x3","x4","x5",],self.domain)
        self.solutions=solutions
        self.words=words
        self.goal=goal
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
    
    def getFeedback(self,guess,solution):
        #Currently this will only allow guesses branching from those with the green letters in the correct spots and yellow letters in the word
        #this means that it will not make a guess that does not use the information received from the previous guess, which may not be
        #the most efficient way to guess
        #instead we should allow a guess or two that we can ignore the green and yellow letters we've found to narrow down our search
        #domain faster before introducing these constraints to make checks
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
            if(tup["w"] !=guess):
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
            if curScore>maxScore:
                maxScore=curScore
                curGuess=word
        return curGuess
    #simulate playing wordle
    def playGameAlg(self):
        solution = self.goal
        # solution="trait"
        print("Trying to guess: " + solution)
        pool= self.words
        count=0
        #val = True
        while(1):
            guess=random.choice(pool)
            count+=1
            print("Guessing : " + guess)
            if(guess!=solution):
                #self.prob.addConstraint(lambda x: x!=guess,"w")
                self.getFeedback(guess,solution)
                sols= self.prob.getSolutions()
                pool = self.parseOutput(sols,guess)
                print("Left with: " + str(len(pool)) + " possible choices.")            
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

def main():
    solutions=genSolutions()
    words=genWords(solutions)
    goal=random.choice(solutions)
    response = input("Run Wordle Algorithm?\nType A if you want to see an average guess # over 100 tries\nType Q to run over all possible solutions\nType Y/N to run once/cancel")
    if(response == "Y" or response =="y"):
        print("Running wordle algorithm")
        init=Wordle(words,solutions,goal)
        init.playGameAlg()
    elif(response =="A" or response =="a"):
        total=0
        for i in range(100):
            init=Wordle(words,solutions,goal)
            total+=init.playGameAlg()
        print("average # of guesses is: " + str(total/100))
    elif(response =="Q" or response =="q"):
        total=0
        for word in solutions:
            init =Wordle(words, solutions, word)
            total += init.playGameAlg()
        print("Average number of guesses over all solutions is: " +str(total/len(solutions)))
    else:
        return None

if __name__=="__main__":
    main()
