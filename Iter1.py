
import constraint
from constraint import *
import random


class Wordle():
    def __init__(self):
        self.prob = Problem()
        self.domain = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
        self.prob.addVariables(["x1","x2","x3","x4","x5",],self.domain)
        self.solutions=[]
        self.words=[]
        self.genSolutions()
        self.genWords()
        self.playGame()

        
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

    
    
def main():
    response = input("Run Wordle Algorithm? (Y/N): ")
    if(response == "Y" or response =="y"):
        print("Running wordle algorithm")
        init=Wordle()
    else:
        return None

if __name__=="__main__":
    main()
