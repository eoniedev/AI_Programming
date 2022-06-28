from problem import Numeric
def main():
    p = Numeric()
    p.setVariables()
    steepestAscent(p)
    p.describeProblem()
    displaySetting(p)
    p.displayResult()
    p.report()

def steepestAscent(p):
    current = p.randomInit() # 'current' is a list of values
    valueC = p.evaluate(current)
    while True:
        neighbors = p.mutants(current)
        successor, valueS = p.bestOf(neighbors)
        if valueS >= valueC:
            break
        else:
            current = successor
            valueC = valueS
    p.storeResult(current, valueC)



def displaySetting(p):
    print()
    print("Search algorithm: Steepest-Ascent Hill Climbing")
    
main()