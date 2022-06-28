from problem import TSP
import random
def main():
    p = TSP()
    p.setVariables()
    steepestAscent(p)
    p.describeProblem()
    displaySetting()
    p.displayResult()
    p.report()

def steepestAscent(p):
    current = p.randomInit()  
    valueC = p.evaluate(current)
    while True:
        neighbors = p.mutants(current)
        (successor, valueS) = p.bestOf(neighbors)
        if valueS >= valueC:
            break
        else:
            current = successor
            valueC = valueS
    p.storeResult(current, valueC)



def displaySetting():
    print()
    print("Search algorithm: Steepest-Ascent Hill Climbing")


main()
