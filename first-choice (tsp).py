from problem import TSP
import random
LIMIT_STUCK = 100 

def main():
    p = TSP()
    p.setVariables()
    firstChoice(p)
    p.describeProblem()
    displaySetting()
    p.displayResult()
    p.report()

def firstChoice(p):
    current = p.randomInit()   
    valueC = p.evaluate(current)
    i = 0
    while i < LIMIT_STUCK:
        successor = p.randomMutant(current)
        valueS = p.evaluate(successor)
        if valueS < valueC:
            current = successor
            valueC = valueS
            i = 0              # Reset stuck counter
        else:
            i += 1
    p.storeResult(current, valueC)


def displaySetting():
    print()
    print("Search algorithm: First-Choice Hill Climbing")

main()
