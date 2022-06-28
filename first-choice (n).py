from problem import Numeric
LIMIT_STUCK = 100
def main():
    p = Numeric()
    p.setVariables()
    firstChoice(p)
    p.describeProblem()
    displaySetting(p)
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
    p.storeResult(current,valueC)

def displaySetting(p):
    print()
    print("Search algorithm: First-Choice Hill Climbing")
    
main()