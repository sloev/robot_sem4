'''
Created on 21/11/2013

@author: Ivo
'''

from random import randrange
from fileinput import input


class Calculator():
    


    def __init__(self):
        self.wrong = 0
        self.correct = 0 
        
        
    def add(self):
        a = randrange(10)
        b = randrange(10)
        print('What is ' + str(a) + ' + ' + str(b))
        answer = input("Enter your answer: ")
        realAnswer = a + b
        if(answer==realAnswer):
            print('Correct')
            self.correct+=1
        else:
            print('Wrong')
            self.wrong+=1
            
            
    def subtract(self):
        a = randrange(10)
        b = randrange(10)
        print("what is" + str(a) + " - " + str(b))
        answer = input ("enter your answer: ")
        realanswer = a - b
        if(answer==realanswer):
            print("correct")
            self.correct+=1
        else:
            print("wrong")
            self.wrong+=1
            
            
    def pow(self):
        a = randrange(12)
        print("what is: " + str(a) + " ^ " + str(2))
        realanswer =pow(a,2)
        answer = input("enter your answer")
        if(answer==realanswer):
            print("correct")
            self.correct+=1
        else:
            print("wrong")
            self.wrong+=1
        
            
            
     
    
    def multiply(self):
        a = randrange(10)
        b = randrange(10)
        print("what is" +str(a) + " * "  + str(b))
        realanswer = a * b
        answer = input ("enter your answer")
        if(answer==realanswer):
            print("correct")
            self.correct+=1
        else:
            print("wrong")
            self.wrong+=1
            
                
    def divide(self):
        a = randrange
        b = randrange
        print("what is" + str(a) + " / " + str(b))
        realanswer = a / b
        answer = input ("enter your answer")
        if(answer==realanswer):
            print("correct")
            self.correct+=1
        else:
            print("wrong")
            self.wrong+=1
            
            
    
    
    def calculations(self):
        
        print("Welcome to Daniel Hansen calculator!")
        print(" ")
        number = input("How many calculations do you want?")
        print("1: addition")
        print("2: subtraction")
        print("3: multiplication")
        print("4: division")
        print("5: pow")
        print(" ")
        choice = input("Enter your choice: ")
         
        if(choice==1):
            for i in range(number):
                self.add()
        elif(choice==2):
            for i in range(number):
                self.subtract()
        elif(choice==3):
            for i in range(number):
                self.multiply()
        elif(choice==4):
            for i in range(number):
                self.divide()
        elif(choice==5):
            for i in range(number):
                self.pow()                
        else:
            print("Invalid number!")
        
        print("you had"+str(self.correct)+"correct answers")
        print("you had"+str(self.wrong)+"wrong answers")
                
    
def main():
    calculater=Calculator()
    calculater.calculations()
    
if __name__ == '__main__':
    main()
        