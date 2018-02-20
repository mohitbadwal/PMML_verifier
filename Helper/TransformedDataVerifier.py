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

    def __rowLevelVerifier(self, column1, column2, column):

        # initial check for number of rows.
        if len(column1) != len(column2):
            return False, 'Length of the number of rows in ' + column + ' don\'t match'

        # check whether content of both columns are equal , if not equal then column order is different or transformed
        # data is different or row order is different
        for i in range(len(column1)):
            if str(column1[i]) != str(column2[i]):
                return False, 'Data in ' + column + ' don\'t match , check if the data is ' \
                                                    'transformed properly or if the columns are ' \
                                                    'in ' \
                                                    'order or whether the rows are in order.'
        return True, ''

    def verifier(self):
        # initializing check variables , total checks = 3
        check = 0

        # Check - 1,2,3
        for column in self.dataset1.columns:
            isVerificationCorrect, reasonString = self.__rowLevelVerifier(self.dataset2[column], self.dataset2[column],
                                                                          column)
            if not isVerificationCorrect:
                print(reasonString)
                return check

        # passed 3 tests before predictions setting check to 3
        check = 3

        return check

