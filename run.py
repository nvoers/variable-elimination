"""
@Author: Joris van Vugt, Moira Berens, Leonieke van den Bulk

Entry point for the creation of the variable elimination algorithm in Python 3.
Code to read in Bayesian Networks has been provided. We assume you have installed the pandas package.

"""

# Nick van Oers, s1009378
# Jord Cluitmans, s1052807
from read_bayesnet import BayesNet
from variable_elim import VariableElimination

if __name__ == '__main__':
    # The class BayesNet represents a Bayesian network from a .bif file in several variables
    net = BayesNet('earthquake.bif') # Format and other networks can be found on http://www.bnlearn.com/bnrepository/
    
    # These are the variables read from the network that should be used for variable elimination
    print("Nodes:")
    print(net.nodes)
    print("Values:")
    print(net.values)
    print("Parents:")
    print(net.parents)
    print("Probabilities:")
    print(net.probabilities)

    # Make your variable elimination code in a seperate file: 'variable_elim'. 
    # You can call this file as follows:
    ve = VariableElimination(net, "log.txt")

    # Set the node to be queried as follows:
    print("Variables: ")
    print(net.nodes)
    query = input("Please enter the query variable: ")

    # The evidence is represented in the following way (can also be empty when there is no evidence):
    evidence = {}
    while True:
        print("Variables: ")
        print(net.nodes)
        var = input("Enter a variable to be added to the evidence, press RETURN to continue: ")
        if var == "":
            break
        print("Values: ")
        print(net.values[var])
        val = input("Enter a value for the variable: ")
        evidence[var] = val
    # Determine your elimination ordering before you call the run function. The elimination ordering   
    # is either specified by a list or a heuristic function that determines the elimination ordering
    # given the network. Experimentation with different heuristics will earn bonus points. The elimination
    # ordering can for example be set as follows:
    elim_order = ve.eliminationOrdering(query)

    # Call the variable elimination function for the queried node given the evidence and the elimination ordering as
    # follows:
    print(ve.run(query, evidence, elim_order))
    ve.close()


