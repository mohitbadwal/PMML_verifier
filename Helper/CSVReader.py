"""
    CSVReader.py created by mohit.badwal
    on 2/20/2018
    
"""

'''
Test class created for reading CSV
'''

import pandas as pd


class CSVReader():
    def read_csv(self, csv_path, sep=',', encoding='cp1256'):
        dataset = pd.read_csv(csv_path, sep=sep, encoding=encoding)
        return dataset