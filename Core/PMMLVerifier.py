"""
    PMMLVerifier.py created by mohit.badwal
    on 2/20/2018
    
"""
from Helper.CSVReader import CSVReader
from Helper.TransformedDataVerifier import TransformedDataVerifier


class PMMLVerifier:
    # format pythonCSV path , PMMLCSV path , Python
    def __init__(self, pythonCsv, pmmlCsv, modelObject, **options):
        # initializing variables for CSV reading
        sep1 = sep2 = ','
        encoding1 = encoding2 = 'cp1256'

        # getting options
        sep1 = options.get('sep1', sep1)
        sep2 = options.get('sep2', sep2)
        encoding1 = options.get('encoding1', encoding1)
        encoding2 = options.get('encoding2', encoding2)

        # converting CSV to pandas dataFrame
        self.pythonDataset = CSVReader().read_csv(pythonCsv, sep=sep1, encoding=encoding1)
        self.pmmlDataset = CSVReader().read_csv(pmmlCsv, sep=sep2, encoding=encoding2)

        # getting modelObject
        self.modelObject = modelObject

    def __transformVerification(self):
        check = TransformedDataVerifier(self.pythonDataset, self.pmmlDataset).verifier()
        if check == 0:
            raise ValueError("The Transformed data does not match")
        return check

    def verify(self):
        self.__transformVerification()
