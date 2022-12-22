"""
@Author: Joris van Vugt, Moira Berens, Leonieke van den Bulk

Class for the implementation of the variable elimination algorithm.

"""

from factor import Factor
import os


class VariableElimination:

    def __init__(self, network, file):
        """
        Initialize the variable elimination algorithm with the specified network.
        Add more initializations if necessary.

        """
        os.remove(file)
        self.file = open(file, "a")
        self.network = network

    def run(self, query, observed, eliminationOrder):
        """
        Use the variable elimination algorithm to find out the probability
        distribution of the query variable given the observed variables

        Input:
            query:      The query variable
            observed:   A dictionary of the observed variables {variable: value}
            eliminationOrder: A list specifying the elimination ordering

        Output: A factor holding the probability distribution
                for the query variable

        """

        self.file.write("Starting with query=" + query + ", observed=" + str(observed) + " and elimination ordering=" + str(eliminationOrder) + ".\n")
        notReduced = [Factor(x, self.network) for x in self.network.probabilities.values()]
        self.file.write("Required factors: \n" + str(notReduced) + "\n")
        factorsCopy = self.reduceFactors(notReduced, observed)
        self.file.write("Reduced factors: \n" + str(factorsCopy) + "\n")

        for variable in eliminationOrder + [query]:
            self.file.write("Variable to be eliminated: " + variable + "\n")
            toMultiply = []
            for factor in factorsCopy:
                contains = False
                for column in factor.table.columns.values[:-1]:
                    if column == variable:
                        contains = True
                if contains:
                    self.file.write("Factor " + str(factor) + " added to multiplication list.\n")
                    toMultiply = toMultiply + [factor]

            for factor in toMultiply:
                factorsCopy.remove(factor)
            if len(toMultiply) >= 1:
                newFactor = toMultiply.pop()
                while len(toMultiply) > 0:
                    newFactor = newFactor.product(toMultiply.pop())
                self.file.write("After multiplication: " + str(newFactor) + "\n")
                if variable is not query:
                    newFactor = newFactor.marginalize(variable)
                    self.file.write("After marginalization: " + str(newFactor) + "\n")
                factorsCopy = factorsCopy + [newFactor]
                self.file.write("Resulting factor: " + str(newFactor) + "\n")
            self.file.write("Factors after elimination of " + variable + ": " + str(factorsCopy) + "\n")

        returnValue = factorsCopy[0]
        returnValue = self.normalizeFactor(returnValue)
        self.file.write("Done!")
        return returnValue

    def normalizeFactor(self, factor):
        """
        Normalizes a factor
        
        return: a new normalized factor
        """
        column = factor.getValues('prob')
        total = 0
        for val in column:
            total = total + val
        mult = 1/total
        for x in range(0, len(factor.table.index)):
            factor.table.loc[x, 'prob'] = factor.table.loc[x, 'prob']*mult
        return factor

    def neededVariables(self, query, observed):
        """
        Computes the variables that are needed for a query given already observed variables
        
        return: all variables in list form that are needed for this computation
        """
        toAdd = {}

        self.getParents(toAdd, query, observed)
        for evidence in list(observed.keys()):
            if evidence not in list(toAdd.keys()):
                self.getParents(toAdd, evidence, observed)

        return list(toAdd.values())

    def eliminationOrdering(self, queryVariable):
        """
        Computes an elimination ordering
        
        return: a list which specifies the elimination ordering
        """
        return [x for x in self.network.probabilities if x != queryVariable]

    def getParents(self, factors, node, observed):
        """
        Computes the parents of a specified node
        
        return: all parents of node
        """
        factors[node] = Factor(self.network.probabilities[node], self.network)
        for parent in self.network.parents[node]:
            if parent not in list(factors.keys()) and parent not in list(observed.keys()):
                self.getParents(factors, parent, observed)

    def reduceFactors(self, factorsCopy, observed):
        """
        Reduces all factors with respect to the observed variables
        
        return: a list of reduced factors
        """
        value = []
        for factor in factorsCopy:
            reducedFactor = factor
            for key in list(observed.keys()):
                reducedFactor = reducedFactor.reduce(key, observed[key])
            value = value + [reducedFactor]
        return value

    def close(self):
        self.file.close()
