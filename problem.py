import random
import math
from sympy import symbols, diff
class Problem:
    def __init__(self):
        self.solution = []
        self.value = 0
        self.numEval = 0
    def setVariables(self):
        pass
    def randomInit(self):
        pass
    def evaluate(self):
        pass
    def mutants(self):
        pass
    def randomMutant(self, current):
        pass
    def describe(self):
        pass
    def storeResult(self, solution, value):
        self.solution = solution
        self.value = value
    def displayResult(self):
        pass
    def report(self):
        print()
        print("Total number of evaluations:",self.numEval)

class Numeric(Problem):
    def __init__(self):
        super().__init__()
        self.DELTA = 0.01
        self.expression = ""
        self.domain = []
        
    def setVariables(self):
        file = input("Enter the file name of a function: ")
        infile = open(file, 'r')
        varNames = []
        low = []
        up = []
        self.expression = infile.readline()
        for file in infile:
            var_, low_, up_ = file.rstrip().split(",")
            varNames.append(var_)
            low.append(float(low_))
            up.append(float(up_))
        self.domain = [varNames, low, up]
    def randomInit(self):
        init = []
        varNames, low, up = self.domain
        for i in range(len(varNames)):
            init.append(random.uniform(low[i],up[i]))
        return init
    def evaluate(self, current):
        self.numEval += 1
        expr = self.expression         # p[0] is function expression
        varNames = self.domain[0]  # p[1] is domain: [varNames, low, up]
        for i in range(len(varNames)):
            assignment = varNames[i] + '=' + str(current[i])
            exec(assignment)
        return eval(expr)
    def mutate(self, current, i, d):
        curCopy = current[:]
        l = self.domain[1][i]     # Lower bound of i-th
        u = self.domain[2][i]     # Upper bound of i-th
        if l <= (curCopy[i] + d) <= u:
            curCopy[i] += d
        return curCopy
    def randomMutant(self, current):
        i = random.randrange(0, len(current))
        d = random.choice([self.DELTA, -self.DELTA])
        return self.mutate(current, i, d)

    def mutants(self, current): ###
        neighbors = []
        for i in range(len(current)):
            successor = self.mutate(current, i, -self.DELTA) 
            neighbors.append(successor)
        
            successor = self.mutate(current, i, self.DELTA) 
            neighbors.append(successor)
        return neighbors     # Return a set of successors
    
    def bestOf(self,neighbors): ###
        best = min(neighbors, key= lambda n: self.evaluate(n))
        bestValue = self.evaluate(best)
        return best, bestValue

    def describeProblem(self):
        print()
        print("Objective function:")
        print(self.expression)   # Expression
        print("Search space:")
        varNames = self.domain[0] # p[1] is domain: [VarNames, low, up]
        low = self.domain[1]
        up = self.domain[2]
        for i in range(len(low)):
            print(" " + varNames[i] + ":", (low[i], up[i])) 
    def displayResult(self):
        print()
        print("Mutation step size:", self.DELTA)
        print()
        print("Solution found:")
        print(self.coordinate())  # Convert list to tuple
        print("Minimum value: {0:,.3f}".format(self.value))
    def coordinate(self):
        c = [round(value, 3) for value in self.solution]
        return tuple(c)  # Convert the list to a tuple
    def takeStep(self, current, value):
        stepSize = 0.01
        i = random.randrange(0, len(current))
        df = diff(self.expression, self.domain[0][i])
        for i in range(len(current)):
            assignment = self.domain[0][i] + '=' + str(current[i])
            exec(assignment)
        ret = eval(str(df))
        if self.domain[1][i] <= (current[i] - stepSize*ret) <= self.domain[2][i]:
            current[i] = current[i] - stepSize*ret
        return current

class TSP(Problem):
    def __init__(self):
        super().__init__()
        self.numCities = 0
        self.locations = []
        self.table = []
    def setVariables(self):
        fileName = input("Enter the file name of a TSP: ")
        infile = open(fileName, 'r')
        # First line is number of cities
        self.numCities = int(infile.readline())
        line = infile.readline()  # The rest of the lines are locations
        while line != '':
            self.locations.append(eval(line)) # Make a tuple and append
            line = infile.readline()
        infile.close()
        self.calcDistanceTable()
        

    def calcDistanceTable(self): ###
        for i in range(self.numCities):
            subTable= []
            
            for j in range(self.numCities):
                dist = round(math.sqrt((self.locations[i][0]-self.locations[j][0])**2 + (self.locations[i][1]-self.locations[j][1])**2),1) 
                subTable.append(dist)
            self.table.append(subTable)
        # A symmetric matrix of pairwise distances
    def mutants(self, current): # Apply inversion
        n = self.numCities
        neighbors = []
        count = 0
        triedPairs = []
        while count <= n:  # Pick two random loci for inversion
            i, j = sorted([random.randrange(n) for _ in range(2)])
            if i < j and [i, j] not in triedPairs:
                triedPairs.append([i, j])
                curCopy = self.inversion(current, i, j)
                count += 1
                neighbors.append(curCopy)
        return neighbors
    def randomMutant(self, current): # Apply inversion
        while True:
            i, j = sorted([random.randrange(self.numCities)
                        for _ in range(2)])
            if i < j:
                curCopy = self.inversion(current, i, j)
                break
        return curCopy
    def bestOf(self, neighbors): ###
        best = min(neighbors, key= lambda n: self.evaluate(n))
        bestValue = self.evaluate(best)
        return best, bestValue
    def randomInit(self):   # Return a random initial tour
        n = self.numCities
        init = list(range(n))
        random.shuffle(init)
        return init

    def evaluate(self, current): ###
        self.numEval += 1
        cost = 0
        for i in range(len(current)-1):
            cost += self.table[current[i]][current[i+1]]
        return cost

    def describeProblem(self):
        print()
        n = self.numCities
        print("Number of cities:", n)
        print("City locations:")
        
        for i in range(n):
            print("{0:>12}".format(str(self.locations[i])), end = '')
            if i % 5 == 4:
                print()

    def inversion(self, current, i, j):  # Perform inversion
        curCopy = current[:]
        while i < j:
            curCopy[i], curCopy[j] = curCopy[j], curCopy[i]
            i += 1
            j -= 1
        return curCopy

    def displayResult(self):
        print()
        print("Best order of visits:")
        self.tenPerRow()       # Print 10 cities per row
        print("Minimum tour cost: {0:,}".format(round(self.value)))
        
    def tenPerRow(self):
        for i in range(len(self.solution)):
            print("{0:>5}".format(self.solution[i]), end='')
            if i % 10 == 9:
                print()
