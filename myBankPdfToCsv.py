# importing required modules 
from PyPDF2 import PdfReader, PdfMerger
# import OS module
import os
import re

#exclusions (index, [value1, value2, ...])
def pdfToCsv(inputPdfName, outputFileName, accountName, headers, pattern, exclusions=None):
    reader = PdfReader(inputPdfName, strict=False)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    #print(text)
    #with open(outputFileName,'w') as f:
    #    f.write(text)
        
    p = re.compile(pattern)
    transactions=re.findall(pattern, text)
    #print(transactions)
    
    with open(outputFileName, 'w') as f:
        headers.insert(0,accountName)
        f.write(', '.join(headers)+"\n")
        class excludeLine(Exception):
            pass
        for transaction in transactions:
            try:
                if exclusions:
                    for (colIndex, values) in exclusions:
                        if transaction[colIndex] in values:
                            raise excludeLine
                transactionStr=', '.join(transaction)
                if 'QUICK FUEL' in transaction:
                    print(transaction)
                f.write(accountName+', '+transactionStr+"\n")
            except excludeLine:
                continue

def dirOfPdfsToCSV(dir_path, outputFile, accountName, headers, pattern, exclusions=None):
    if dir_path[len(dir_path)-1]!='\\':
        dir_path+='\\'
        
    pdfMerge=PdfMerger()#f)
    with open(outputFile, "w") as f:
        #pageCount=0
        filenames = os.listdir(dir_path)
        filepaths = [dir_path+x for x in filenames]
        for i in range(len(filenames)):
            #reader = PdfReader(filepaths[i])
            pdfMerge.append(filepaths[i])
            #pageCount+=reader.pages
    pdfMerge.write(outputFile[:-4]+".tmp")
    pdfToCsv(outputFile[:-4]+".tmp", outputFile, accountName, headers, pattern, exclusions)

if __name__ == '__main__':

    accountName='pnc_credit_card'
    pattern=r'([0-9]{2}\/[0-9]{2})\s([0-9]{2}\/[0-9]{2})\s(.*?)\s(\-?\$[0-9\.]*)'
    dirOfPdfsToCSV(r'C:\Users\GPS Tablet User\Curry Personal\pnc_credit_card_statements', r'combinedPncCreditCardStatements.csv', 'pnc_credit_card',['Transaction date', 'Date posted', 'Description', 'Amount'], pattern)
         