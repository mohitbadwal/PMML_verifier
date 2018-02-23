"""
    PredictionsVerifier.py created by mohit.badwal
    on 2/20/2018
    
"""
import numpy as np


class PredictionsVerifier:
    def __init__(self, predictions1, predictions2):
        """
            :param predictions1: first predictions pandas DataFrame
            :param predictions2: second predictions pandas DataFrame
        """
        self.__predictions1 = predictions1
        self.__predictions2 = predictions2

    def __rowLevelVerifier(self, column1, column2, column1Name, column2Name):
        tempCheck = 0
        # initial check for number of rows.
        if len(column1) != len(column2):
            return False, 'Length of the number of rows in  don\'t match'

        # check if names of column1 and column2 match
        if str(column2Name) != str(column1Name):
            tempCheck = -1

        # setting floating point to 5
        if column1.dtype == column2.dtype == np.float64:
            column1 = column1.apply(lambda x: round(x, 5))
            column2 = column2.apply(lambda x: round(x, 5))

        # check if the results and probabilities match
        rowCheck = column1.eq(column2)
        uniqueRowChecks = rowCheck.unique()
        if len(uniqueRowChecks) != 1 or not uniqueRowChecks[0]:
            return False, 'The hyper params for the models don\'t match'

        return True, ''

    def verifier(self):

        # initializing check variables , total checks = 3
        check = 0
        # check whether number of columns in both CSV are equal
        if len(self.__predictions1.columns) != len(self.__predictions2.columns):
            s = "The number of columns are not equal in the two datasets."
            print(s)
            return check, s
        # Check - 1,2,3
        for i in range(len(self.__predictions1.columns)):
            isVerificationCorrect, reasonString = self.__rowLevelVerifier(self.__predictions1.iloc[:, i],
                                                                          self.__predictions2.iloc[:, i],
                                                                          self.__predictions1.columns[i],
                                                                          self.__predictions2.columns[i])
            if not isVerificationCorrect:
                print(reasonString)
                return check, reasonString

        # passed 3 tests before predictions setting check to 3
        check = 3

        return check, ''
