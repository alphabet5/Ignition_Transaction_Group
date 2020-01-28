#import xml.etree.ElementTree as ET
from lxml import etree
from csv import DictReader
from xmljson import badgerfish as bf
from copy import deepcopy

def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

datatypes = {'Byte': 0, 'Int1': 0,
             'Short': 1, 'Int2': 1,
             'Integer': 2, 'Int4': 2,
             'Long': 3, 'Int8': 3,
             'Float': 4, 'Float4': 4,
             'Double': 5, 'Float8': 5,
             'Boolean': 6,
             'String': 7,
             'DateTime': 8,
             'Text': 10,
             'Byte Array': 17, 'Int1Array': 17,
             'Short Array': 18, 'Int2Array': 18,
             'Integer Array': 11, 'Int4Array': 11,
             'Long Array': 12, 'Int8Array': 12,
             'Float Array': 19, 'Float4Array': 19,
             'Double Array': 13, 'Float8Array': 13,
             'Boolean Array': 14, 'BooleanArray': 14,
             'String Array': 15, 'StringArray': 15,
             'DateTimeArray': 16,
             'ByteArray': 20,
             'Dataset': 9, 'DataSet': 9,
             'Document': 29}

if __name__ == '__main__':
    base = etree.fromstring(open('TransactionGroup.xml', 'r').read())
    obj = bf.data(base)
    # template
    t = obj['Project']['Groups']['GroupConfig']['Property'][0]['ItemConfig'][0]
    filepath = 'TransactionGroup.csv'
    csv_data = DictReader(open(filepath))
    items = list()
    for row in csv_data:
        t['@name'] = row['name']
        for i in range(len(t['Property'])):
            if t['Property'][i]['@name'] == 'TARGET_DATA_TYPE':
                if is_int(row['datatype']):
                    dt = row['datatype']
                elif row['datatype'] in datatypes.keys():
                    dt = datatypes[row['datatype']]
                else:
                    print("Error with datatype on row: " + row['name'])
                    dt = t['Property'][i]['$']
                t['Property'][i]['$'] = dt
            if t['Property'][i]['@name'] == 'OPCITEMPATH':
                t['Property'][i]['$'] = row['opcitempath']
            if t['Property'][i]['@name'] == 'TARGET_NAME':
                t['Property'][i]['$'] = row['target']
        items.append(deepcopy(t))
    obj['Project']['Groups']['GroupConfig']['Property'][0]['ItemConfig'] = items

    with open('TransactionGroupOutput.xml', 'wb') as f:
        f.write(etree.tostring(bf.etree(obj)[0], pretty_print=True))
