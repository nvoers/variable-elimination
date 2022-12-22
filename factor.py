import pandas as pd
from read_bayesnet import BayesNet


class Factor:

    def __init__(self, table: pd.DataFrame, net: BayesNet):
        self.table = table
        self.net = net

    def product(self, factor):
        """
        Computes the product of this factor and the factor parameter

        return: A new factor
        """
        variables = []
        for col in self.table.columns.values[:-1]:
            variables = variables + [col]
        for col in factor.table.columns.values[:-1]:
            if col not in variables:
                variables = variables + [col]

        df = pd.DataFrame(columns=variables + ['prob'])

        self.fillDataframe(df, variables, [], factor)

        return Factor(df, self.net)

    def fillDataframe(self, dataframe: pd.DataFrame, variables, values, factor):
        """
        Computes the product of a vector by recursively filling the dataframe parameter
        """
        if len(values) == len(variables):
            dict = {}
            for i in range(0, len(variables)):
                dict[variables[i]] = values[i]

            prob1 = self.getProbability(dict)
            prob2 = factor.getProbability(dict)
            dataframe.loc[len(dataframe)] = values + [prob1 * prob2]
        else:
            current_variable = variables[len(values)]
            all_values = self.getValues(current_variable)
            if all_values is None:
                all_values = factor.getValues(current_variable)
            for value in all_values:
                self.fillDataframe(dataframe, variables, values + [value], factor)

    def getProbability(self, dict: dict) -> float:
        """
        Returns probability of variables which values correspond to the dict values
        
        return: probability of the specified variables
        """
        cols = self.table.columns.values[:-1]
        for row in [self.table.iloc[i] for i in range(0, len(self.table))]:
            cont = True
            for col in cols:
                if row[col] != dict[col]:
                    cont = False
                    pass

            if cont:
                return row['prob']

    def getValues(self, col):
        """
        Retuns all values of a column as a list

        return: values of a column
        """
        colIndex = self.columnIndex(col)
        if colIndex is not None:
            values = self.table.iloc[:, colIndex].tolist()
            output = []
            for x in values:
                if x not in output:
                    output = output + [x]
            return output
        else:
            return None

    def columnIndex(self, col):
        """
        Returns the index of a specific column in a factor

        return: the index of the column
        """
        for i in range(0, len(self.table.columns.values)):
            if col == self.table.columns.values[i]:
                return i
        return None

    def marginalize(self, variable):
        """
        Marginalize this factor

        return: a new factor with variable marginalized
        """
        newCols = [x for x in self.table.columns.values if x != variable and x != 'prob']
        df = pd.DataFrame(columns=newCols + ['prob'])

        self.summation(df, newCols, [])
        return Factor(df, self.net)

    def summation(self, dataframe: pd.DataFrame, variables, values):
        """
        Function used for summing up probabilities from the dataframe of this factor
        """
        if len(values) == len(variables):
            dict = {}
            for i in range(0, len(variables)):
                dict[variables[i]] = values[i]
            sum = self.getSumProbability(dict)
            dataframe.loc[len(dataframe)] = values + [sum]
        else:
            current_variable = variables[len(values)]
            all_values = self.getValues(current_variable)
            for value in all_values:
                self.summation(dataframe, variables, values + [value])

    def getSumProbability(self, dict: dict) -> float:
        """
        Get the sum of a probability corresponding to all variable values in dict

        return: a summation of all variables in dict
        """
        cols = self.table.columns.values[:-1]
        add = 0
        for row in [self.table.iloc[i] for i in range(0, len(self.table))]:
            cont = True
            for col in cols:
                if col in dict.keys():
                    if row[col] != dict[col]:
                        cont = False
                        pass
            if cont:
                add = add + row['prob']

        return add

    def reduce(self, variable, value):
        """
        Reduce a variable into this factor

        return: a new factor with the variable reduced
        """
        if value not in self.net.values[variable]:
            raise Exception("Unknown value for variable")

        if variable not in self.table.columns.values:
            return self

        df = self.table[self.table[variable] == value]

        return Factor(df, self.net)

    def __str__(self):
        columns = self.table.columns.values[:-1]
        ret = "Factor with: " + str(columns) + "\n" + str(self.table) + "\n"
        return ret

    def __repr__(self):
        columns = self.table.columns.values[:-1]
        ret = "\nFactor with: " + str(columns) + "\n" + str(self.table)
        return ret
