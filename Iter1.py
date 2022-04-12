
import constraint
from constraint import *
import random



class Wordle():
    def __init__(self):
        self.prob = Problem()
        #self.domain = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
        #self.prob.addVariables(["x1","x2","x3","x4","x5",],self.domain)
        self.solutions=[]
        self.words=[]
        self.genSolutions()
        self.genWords()
        print("Starting with: " + str(len(self.words)) + " possible words")
        self.prob.addVariable("w",self.words)
        # self.prob.addConstraint(lambda x: x in self.words,"w")
        # self.prob.addConstraint(lambda x: x[0]=='a',"w")
        # x=self.prob.getSolutions()
        # self.prob.addConstraint(lambda x: x[1]=='b',"w")
        # x=self.prob.getSolutions()
        #print(x)


        
        #read in all possible solutions
    def genSolutions(self):
        answerFile = open("words.txt","r")
        data = answerFile.readlines()
        print("imported " + str(len(data)) + " words from input file")
        answerFile.close()

        #store all words in array, strip the newline characters off the end of them
        for word in data:
            self.solutions.append(word.strip())

    def genWords(self):
        #read in list of english words
        wordFile = open("english_words.txt")
        data = wordFile.readlines()
        print("imported " + str(len(data)) + " words from english_words.txt")
        wordFile.close()

        #store all of these stripped words of length 5 in an array
        for word in data:
            x=word.strip()
            if(len(x)==5):
                self.words.append(x)
        print(str(len(self.words)) + " remain after eliminating non-5 letter words")

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
        #if statements are "green" feedback, so letter is in the right spot
        #elif statements are "yellow" feedback, so letter is somewhere in the word
        #else statements are "black" feedback, so letter is not in the word
        if( g1== s1 ):
            self.prob.addConstraint(lambda x: x[0]==g1, "w")
        elif(g1 in solution):
            self.prob.addConstraint(lambda x : g1 in x, "w")
        else: 
            self.prob.addConstraint(lambda x: g1 not in x, "w")
        if( g2== s2 ):
            self.prob.addConstraint(lambda x: x[1]==g2, "w")
        elif(g2 in solution):
            self.prob.addConstraint(lambda x : g2 in x, "w")
        else: 
            self.prob.addConstraint(lambda x: g2 not in x, "w")
        if( g3== s3 ):
            self.prob.addConstraint(lambda x: x[2]==g3, "w")
        elif(g3 in solution):
            self.prob.addConstraint(lambda x : g3 in x, "w")
        else: 
            self.prob.addConstraint(lambda x: g3 not in x, "w")
        if( g4== s4 ):
            self.prob.addConstraint(lambda x: x[3]==g4, "w")
        elif(g4 in solution):
            self.prob.addConstraint(lambda x : g4 in x, "w")
        else: 
            self.prob.addConstraint(lambda x: g4 not in x, "w")
        if( g5== s5 ):
            self.prob.addConstraint(lambda x: x[4]==g5, "w")
        elif(g5 in solution):
            self.prob.addConstraint(lambda x : g5 in x, "w")
        else: 
            self.prob.addConstraint(lambda x: g5 not in x, "w")

    #read solution output into list
    #this elimates words from the possible list of guesses
    def parseOutput(self,input):
        newPool=[]
        for tup in input:
            newPool.append(tup["w"])
        return newPool

    #simulate playing wordle
    def playGameAlg(self):
        solution = random.choice(self.solutions)
        print("Trying to guess: " + solution)
        pool= self.words
        count=0
        guess="crane"
        #val = True
        while(1):
            print("Guessing : " + guess)
            count+=1
            if(guess!=solution):
                #self.prob.addConstraint(lambda x: x!=guess,"w")
                self.getFeedback(guess,solution)
                sols= self.prob.getSolutions()
                pool = self.parseOutput(sols)
                print("Left with: " + str(len(pool)) + " possible choices.")
                guess=random.choice(pool)
            else:
                print("Found answer in: " + str(count) + " tries.")
    
                break
        return count
    
def main():
    response = input("Run Wordle Algorithm? (Y/N): Type A if you want to see an average guess # over 100 tries ")
    if(response == "Y" or response =="y"):
        print("Running wordle algorithm")
        init=Wordle()
        init.playGameAlg()
    elif(response =="A" or response =="a"):
        total=0
        for i in range(100):
            init=Wordle()
            total+=init.playGameAlg()
        print("average # of guesses is: " + str(total/100))
    else:
        return None

if __name__=="__main__":
    main()
