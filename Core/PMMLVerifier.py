"""
    PMMLVerifier.py created by mohit.badwal
    on 2/20/2018
    
"""
from Helper.CSVReader import CSVReader
from Helper.PredictionsVerifier import PredictionsVerifier
from Helper.TransformedDataVerifier import TransformedDataVerifier
import pandas as pd


class PMMLVerifier:
    # format pythonCSV path or dataFrame , PMMLCSV path or dataFrame , model object and options
    # the train CSV's dhould only have the transformed data
    # the test CSV's should have this pattern (transformed data , predictions , [probabilities]) for classification
    # for regression (transformed data , predictions)
    def __init__(self, pythonCsv, pmmlCsv, checkFor='test', problemType='classification', **options):

        """
                    :param pythonCsv: CSV path for python file or DataFrame object
                    :param pmmlCsv: CSV path for pmml file or DataFrame object
                    :param problemType: 'classification' or 'regression' , by default 'classification'
                    :param checkFor: 'test' for testing dataset and 'train' for training dataset
                    :arg options: for multi class set classes=(number of classes) by default 2
                                for setting different separators or encoding for the CSV which are passed ,
                                set sep1 and encoding1 for first CSV and sep2 and encoding2 for second CSV,
                                set rounding param if you want a custom rounding value , default is 5
        """

        # initializing variables for CSV reading
        sep1 = sep2 = ','
        rounding = 5
        encoding1 = encoding2 = 'cp1256'
        classes = 2
        problemTypeList = ['classification', 'regression']
        checkForList = ['train', 'test']

        # check for correct problem type
        if problemType not in problemTypeList:
            raise AttributeError(problemType + ' is not a proper problem type')

        # check for correct CSV type
        if checkFor not in checkForList:
            raise AttributeError(checkFor + ' is not a proper checkFor type')

        # getting options
        sep1 = options.get('sep1', sep1)
        sep2 = options.get('sep2', sep2)
        encoding1 = options.get('encoding1', encoding1)
        encoding2 = options.get('encoding2', encoding2)
        rounding = options.get('rounding', rounding)
        if problemType == 'classification':
            classes = options.get('classes', classes)
        else:
            classes = 0

        # converting CSV to pandas dataFrame if the argument for pythonCSV and pmmlCSV were paths
        if type(pythonCsv) == str:
            self.__pythonDataset = CSVReader().read_csv(pythonCsv, sep=sep1, encoding=encoding1)
        else:
            self.__pythonDataset = pythonCsv

        if type(pmmlCsv) == str:
            self.__pmmlDataset = CSVReader().read_csv(pmmlCsv, sep=sep2, encoding=encoding2)
        else:
            self.__pmmlDataset = pmmlCsv

        self.__checkFor = checkFor
        self.__rounding = rounding

        if checkFor == 'test':
            # putting the predictions to a different DataFrame
            self.__pythonPredictions = self.__pythonDataset.iloc[:, -1:(-2 - classes):-1]
            self.__pmmlPredictions = self.__pmmlDataset.iloc[:, -1:(-2 - classes):-1]

            # getting pure transformed data as a DataFrame
            self.__pythonDataset = self.__pythonDataset.iloc[:, :(-1 - classes)]
            self.__pmmlDataset = self.__pmmlDataset.iloc[:, :(-1 - classes)]

    def __transformVerification(self):
        check, reasonFailure = TransformedDataVerifier(self.__pythonDataset, self.__pmmlDataset,rounding = self.__rounding).verifier()
        # if check was 0 raise an error
        if check == 0:
            raise ValueError(reasonFailure)
        return check

    def __predictionVerification(self):
        check, reasonFailure = PredictionsVerifier(self.__pythonPredictions, self.__pmmlPredictions).verifier()
        # if check was 0 raise an error
        if check == 0:
            raise ValueError(reasonFailure)
        return check

    def verify(self):
        self.__transformVerification()
        if self.__checkFor == 'test':
            self.__predictionVerification()
        print("Verification was Successful")
