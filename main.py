"""
Authors - Nicolas Randazzo | Tony Rago
Course | Professor - CS 454 Theory of Computation | Dr. Balasubramanian Ravikumar
Due Date - 12/17/2023

                        ----------    Description    ----------
        Given two strings x and y of the same length N over a finite alphabet Σ of size M. 
        (N and M are user inputs so your solution should work for arbitrary N and M.) 
        Consider a game involving two players A and B. A random string over the alphabet Σ is generated until x or y appears. 
        (You can assume that x and y do not have a common prefix (other than the null string.) 
        If the game terminates with the appearance of x (y), player 1 (2) wins.
        This program takes as input the strings x and y, and outputs the probability that A wins. 

"""
import numpy as np

class DFA:
    # Class constructor for default DFA setup
    def __init__(self, alphabet) -> None:
        self.alphabet = alphabet
        self.Q = []
        self.S = None
        self.F = None
        self.transition = {}
          
    # Generate DFA states
    def generateStates(self, x, y):
       for i in range(len(x) + len(y) + 1):
            self.Q.append(i)
       self.S = 0
       self.F = len(x)+len(y)
       
    # Generate state transitions from top "row" to bottom "row" 
    def crissCrossTransitions(self, string, otherString, loopStart, loopEnd, k=None):
        for j in range (loopStart, loopEnd, 1):
            if(k):
                pathWeFollowed = string[:k]
            else:
                pathWeFollowed = string[:j]
            
            for symbol in self.alphabet:
                if symbol not in self.delta[j].keys():
                    prefix = pathWeFollowed + symbol

                    while len(prefix) >= 1 and prefix != otherString[:len(prefix)]:
                        if prefix == string[:len(prefix)]:
                            if(k):
                                self.delta[j][symbol] = self.Q[len(string)+len(prefix)]
                            else:
                                self.delta[j][symbol] = self.Q[len(prefix)]
                            break
                        prefix = prefix[1:]

                    if len(prefix) == 0:
                        self.delta[j][symbol] = 0
                    elif symbol in self.delta[j].keys():
                        continue
                    else:
                        if(k):
                            self.delta[j][symbol] = self.Q[len(prefix)]
                        else:
                            self.delta[j][symbol] = self.Q[len(string)+len(prefix)]
                if(k):
                    k+=1


    # Generate state transition "paths" based on strings x and y
    # Then calls function crissCrossTransitions for the rest of state transitions
    def generateDelta(self, x, y) -> None:
        # Delta = {state: {transition: result_state}, state: {transition: result_state}, ... }
        delta = {state: {} for state in self.Q}

        # Generate the path for y 
        for i in range(0, len(y), 1):
            delta[i][str(y[i])] = i+1 

        # No transition on reject state
        for symbol in self.alphabet:
            delta[i+1][symbol] = -1

        last = i + 2 # increment path 'index'

        # Generate path for x
        delta[0][str(x[0])] = last
        
        # Generate path for x
        for i in range(1, len(x), 1):
            delta[last][str(x[i])] = last +1
            last += 1 
        # No transition on accepting state
        for symbol in self.alphabet:
            delta[last][symbol] = -1
        
        # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        # Generates transitions for exactly x and y strings
        
        # Generates all other transitions
        # vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

        for symbol in self.alphabet:
            if symbol not in delta[0].keys():
                delta[0][symbol] = 0

        self.delta = delta
        self.crissCrossTransitions(y, x, 1, len(y)+1)
        self.crissCrossTransitions(x, y, len(x)+1, len(x)+len(y), k=1)
        
    # Create matrix for probability of each state
        # I.E. P0 = 1/3(P0) + 1/3(P1) + 1/3(P4)
    def computeMatrix(self):
        matrix = []
        for state in self.delta:
            arr = [0] * len(self.Q)
            arr[state] = 1

            # if state is accept or reject skip it
            if state == self.F or state == self.F/2:
                matrix.append(arr)
                continue
            
            for symbol in self.alphabet:
                arr[self.delta[state].get(symbol)] -= (1/len(self.alphabet))
            
            matrix.append(arr)
        
        matrix = np.matrix(matrix)
        return matrix
    
    # Inverts matrix and multiplies by identity vector
    # Returns the probability result matrix
    def calculateProbability(self, matrix)-> np.mat:
            b = [0] * len(self.Q)
            b[-1] = 1
            b = np.array(b)
            invMatrix = np.matrix(matrix).I
            result_matrix = np.matmul(invMatrix, b)
            return(result_matrix)

def main() -> None:
    M = input("Enter length of alphabet: ")
    M = int(M)
    sigma = input("Enter alphabet: ")
    sigma = sigma.split()
    while len(sigma) != M:
        sigma = input("Enter alphabet: ")
        sigma = sigma.split()
    N = input("Enter length of strings x and y: ")
    N = int(N)

    x = input("X: ")
    while (len(x) != N):
        x = input("X: ")
    y = input("Y: ")
    while(len(y) != N):
        y = input("Y: ")
  
    # Create DFA Object
    dfa = DFA(sigma)
      
    # Generate the set of states, the starting state, and the accepting state
    dfa.generateStates(x, y)
    
    # Generate Delta function
    dfa.generateDelta(x, y)
    # Sorts the dictionary

    # Generate probability matrix based on transitions out of each stateix basSorts the dictionarydfa.computeMatrix()
    probability_matrix = dfa.computeMatrix()

    # Resulting matrix after inverting and multiplying by probability of Player A String
    game_matrix = dfa.calculateProbability(probability_matrix)

    # Calculate probability of player A winning
    a_prob = 1-game_matrix[0,0]


    print("Probability that Player A wins: ", round(a_prob * 100, 4), '% or: ', a_prob, sep="")


    
main()