"""
    PredictionsVerifier.py created by mohit.badwal
    on 2/20/2018
    
"""


class PredictionsVerifier:
    def __init__(self, predictions1, predictions2):
        """
            :param predictions1: first predictions pandas DataFrame
            :param predictions2: second predictions pandas DataFrame
        """
        self.predictions1 = predictions1
        self.predictions2 = predictions2

    def __rowLevelVerifier(self, column1, column2, column1Name, column2Name):

        tempCheck = 0
        # initial check for number of rows.
        if len(column1) != len(column2):
            return False, 'Length of the number of rows in  don\'t match'

        # check if names of column1 and column2 match
        if str(column2Name) != str(column1Name):
            tempCheck = -1

        # check whether row order is different
        rowOrderCheck = column1.value_counts().eq(column2.value_counts()).unique()
        if len(rowOrderCheck) != 1 or not rowOrderCheck[0]:
            # if the name of the columns were not same and the row order check doesn't match then probably the column
            # order is different.
            if tempCheck == -1:
                return False, 'The column orders for ' + column1Name + ' of python Predictions and column ' + column2Name + \
                       ' of PMML Predictions CSV are not the same'
            return False, 'The hyper params for the models don\'t match'

        # check whether content of both columns are equal , if not equal then column order is different
        # or hyper params are not same
        rowCheck = column1.eq(column2)
        uniqueRowChecks = rowCheck.unique()
        if len(uniqueRowChecks) != 1 or not uniqueRowChecks[0]:
            return False,  'The hyper params for the models don\'t match'

        return True, ''

    def verifier(self):

        # initializing check variables , total checks = 3
        check = 0

        # check whether number of columns in both CSV are equal
        if len(self.dataset1.columns) != len(self.dataset2.columns):
            s = "The number of columns are not equal in the two datasets."
            print(s)
            return check, s
        # Check - 1,2,3
        for i in range(len(self.dataset1.columns)):
            isVerificationCorrect, reasonString = self.__rowLevelVerifier(self.dataset1.iloc[:, i],
                                                                          self.dataset2.iloc[:, i],
                                                                          self.dataset1.columns[i],
                                                                          self.dataset2.columns[i])
            if not isVerificationCorrect:
                print(reasonString)
                return check, reasonString

        # passed 3 tests before predictions setting check to 3
        check = 3

        return check, ''
