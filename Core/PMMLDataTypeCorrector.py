"""
    PMMLDataTypeCorrector.py created by mohit.badwal
    on 2/26/2018
    
"""
from xml.etree import ElementTree

import xmltodict
import numpy as np

from Helper.CSVReader import CSVReader


class PMMLDataTypeCorrector:
    def __init__(self, data, columns, pmmlPath,**options):
        """
        
        :param data: the dataFrame or path to get the dtypes 
        :param columns: the columns which are in PMML including the output column
        :param pmmlPath: path of the pmml
        :arg options: for setting different separators or encoding for the CSV which are passed ,
                        set sep and encoding for CSV 
                                
        """
        sep = ','
        encoding = 'cp1256'
        sep = options.get('sep', sep)
        encoding = options.get('encoding', encoding)
        if type(data) == str:
            self.__dataset = CSVReader().read_csv(data, sep=sep, encoding=encoding)
        self.__dataset = data
        self.__columns = columns
        self.__pmmlPath = pmmlPath

    def __confirm(self, dtype):
        if dtype in [np.int8, np.int16, np.int32, np.int64,
                     np.uint, np.uint8, np.uint16, np.uint32, np.uint64]:
            return 0
        elif dtype in [np.float16, np.float32, np.float64]:
            return 1
        else:
            return 2

    def __matcher(self, dataTypeDict):
        pmmlDataTypes = ['integer', 'double', 'string']
        for column in self.__columns:
            if dataTypeDict[column] in pmmlDataTypes:
                typeReturn = self.__confirm(self.__dataset[column].dtype)
                dataTypeDict[column] = pmmlDataTypes[typeReturn]
        return dataTypeDict

    def correct(self):
        dataTypeDict = {}
        with open(self.__pmmlPath, "rb") as myfile:
            d = xmltodict.parse(myfile, xml_attribs=True)
            dataFields = d['PMML']['DataDictionary']['DataField']
            for dataField in dataFields:
                dataTypeDict[dataField['@name']] = dataField['@dataType']
            dataTypeDict = self.__matcher(dataTypeDict)
        with open(self.__pmmlPath, "r") as myfile:
            data = myfile.readlines()
        dataToWrite = []
        for line in data:
            if str(line).find('DataField') != -1:
                if str(line).find("dataType") != -1:
                    d1 = line.split('name="')[1].split('"')[0]
                    d2 = line.split('optype="')[1].split('"')[0]
                    d3 = '"/>'
                    print(line.strip()[-2])
                    if line.strip()[-2] != '/':
                        d3 = '">'
                    line = '<DataField name="'+d1+'" optype="'+d2+'" dataType="'+dataTypeDict[d1]+d3
            dataToWrite.append(line)
        with open(self.__pmmlPath, "w") as myfile:
            myfile.write(''.join(dataToWrite))
        print("DataTypes were corrected in the PMML")

