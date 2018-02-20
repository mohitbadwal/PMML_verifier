"""
    TransformedDataVerifier.py created by mohit.badwal
    on 2/20/2018
    
"""


class TransformedDataVerifier:
    def __init__(self, dataset1, dataset2) -> None:

        """
            :param dataset1: first pandas DataFrame
            :param dataset2: second pandas DataFrame
        """

        self.dataset1 = dataset1
        self.dataset2 = dataset2

    def __rowLevelVerifier(self, column1, column2, column1Name, column2Name):

        # initial check for number of rows.
        if len(column1) != len(column2):
            return False, 'Length of the number of rows in  don\'t match'

        # check whether content of both columns are equal , if not equal then column order is different or transformed
        # data is different or row order is different
        rowCheck = column1.eq(column2)
        uniqueRowChecks = rowCheck.unique()
        if len(uniqueRowChecks) != 1 or uniqueRowChecks[0] == False:
            return False, 'The data in column ' + column1 + ' of python CSV and column' + column2 + ' of PMMl CSV' \
                                                                                                    'are not same.'

        return True, ''

    def verifier(self):
        # initializing check variables , total checks = 3
        check = 0

        # check whether number of columns in both CSV are equal
        if len(self.dataset1.columns) != len(self.dataset2.columns):
            print("The number of columns are not equal in the two datasets.")
            return check
        # Check - 1,2,3
        for i in range(len(self.dataset1.columns)):
            isVerificationCorrect, reasonString = self.__rowLevelVerifier(self.dataset1.iloc[:, i],
                                                                          self.dataset2.iloc[:, i],
                                                                          self.dataset1.columns[i],
                                                                          self.dataset2.columns[i])
            if not isVerificationCorrect:
                print(reasonString)
                return check

        # passed 3 tests before predictions setting check to 3
        check = 3

        return check
