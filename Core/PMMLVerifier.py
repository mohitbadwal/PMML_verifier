"""
    PMMLVerifier.py created by mohit.badwal
    on 2/20/2018
    
"""
from Helper.CSVReader import CSVReader
from Helper.TransformedDataVerifier import TransformedDataVerifier
import pandas as pd


class PMMLVerifier:
    # format pythonCSV path or dataFrame , PMMLCSV path or dataFrame , model object and options
    def __init(self, pythonCsv, pmmlCsv, **options):
        # initializing variables for CSV reading
        sep1 = sep2 = ','
        encoding1 = encoding2 = 'cp1256'

        # getting options
        sep1 = options.get('sep1', sep1)
        sep2 = options.get('sep2', sep2)
        encoding1 = options.get('encoding1', encoding1)
        encoding2 = options.get('encoding2', encoding2)

        # converting CSV to pandas dataFrame if the argument for pythonCSV and pmmlCSV were paths
        if type(pythonCsv) == str:
            self.pythonDataset = CSVReader().read_csv(pythonCsv, sep=sep1, encoding=encoding1)
        else:
            self.pythonDataset = pythonCsv

        if type(pmmlCsv) == str:
            self.pmmlDataset = CSVReader().read_csv(pmmlCsv, sep=sep2, encoding=encoding2)
        else:
            self.pmmlDataset = pmmlCsv

        # getting modelObject

    def __transformVerification(self):
        check = TransformedDataVerifier(self.pythonDataset, self.pmmlDataset).verifier()
        # if check was 0 raise an error
        if check == 0:
            raise ValueError("The Transformed data does not match")
        return check

    def verify(self):
        self.__transformVerification()
