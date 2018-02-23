"""
    TransformedDataVerifier.py created by mohit.badwal
    on 2/20/2018
    
"""

import numpy as np


class TransformedDataVerifier:
    def __init__(self, dataset1, dataset2, rounding) -> None:

        """
            :param dataset1: first pandas DataFrame
            :param dataset2: second pandas DataFrame
        """

        self.__dataset1 = dataset1
        self.__dataset2 = dataset2
        self.__rounding = rounding

    def __rowLevelVerifier(self, column1, column2, column1Name, column2Name):

        tempCheck = 0
        # initial check for number of rows.
        if len(column1) != len(column2):
            return False, 'Length of the number of rows in  don\'t match'

        # check if the dtypes are same
        if column1.dtype != column2.dtype:
            print('The data type for ' + column1Name + ' of python CSV and column ' + column2Name + ' of PMML CSV' \
                                                                                                    ' are not same.')

        # check if names of column1 and column2 match
        if str(column2Name) != str(column1Name):
            tempCheck = -1

            # setting floating point to 5
            if column1.dtype == column2.dtype == np.float64:
                column1 = column1.apply(lambda x: round(x, self.__rounding))
                column2 = column2.apply(lambda x: round(x, self.__rounding))

        # check whether row order is different
        rowOrderCheck = column1.value_counts().eq(column2.value_counts()).unique()
        if len(rowOrderCheck) != 1 or not rowOrderCheck[0]:
            # if the name of the columns were not same and the row order check doesn't match then probably the column
            # order is different.
            if tempCheck == -1:
                return False, 'The column orders for ' + column1Name + ' of python CSV and column ' + column2Name + 'of PMML CSV' \
                                                                                                                    ' are not same.'
            return False, 'The transformed data for ' + column1Name + ' of python CSV and column ' + column2Name + ' of PMML CSV' \
                                                                                                                   ' are not same. '

        # check whether content of both columns are equal , if not equal then column order is different or transformed
        # transformed data is different
        rowCheck = column1.eq(column2)
        uniqueRowChecks = rowCheck.unique()
        if len(uniqueRowChecks) != 1 or not uniqueRowChecks[0]:
            return False, 'The row order in column ' + column1Name + ' of python CSV and column ' + column2Name + ' of PMML CSV' \
                                                                                                                  ' are not same.'

        return True, ''

    def verifier(self):

        # initializing check variables , total checks = 3
        check = 0

        # check whether number of columns in both CSV are equal
        if len(self.__dataset1.columns) != len(self.__dataset2.columns):
            s = "The number of columns are not equal in the two datasets."
            print(s)
            return check, s
        # Check - 1,2,3
        for i in range(len(self.__dataset1.columns)):
            isVerificationCorrect, reasonString = self.__rowLevelVerifier(self.__dataset1.iloc[:, i],
                                                                          self.__dataset2.iloc[:, i],
                                                                          self.__dataset1.columns[i],
                                                                          self.__dataset2.columns[i])
            if not isVerificationCorrect:
                print(reasonString)
                return check, reasonString

        # passed 3 tests before predictions setting check to 3
        check = 3

        return check, ''
