import csv
import os
def CSVtoTSV(filename):
    # filename='Big_Kahuna.csv'
    tsvfile = open(filename.replace('.csv','.tsv'), 'w+')
    tsvtempfile=csv.writer(tsvfile, delimiter='\t')
    tsvtempfile.writerows(csv.reader(open(filename)))
dir=input("What is the directory with all datefiles in it?")
filelist=os.listdir(dir)
filelist = filter(lambda k:'.csv' in k, filelist)
filelist = filter(lambda k: not 'outputs' in k, filelist)
filelist = list(filter(lambda k: not '_HOST_' in k, filelist))
for name in filelist:
    print("File name " + name + "--------------------------------------")
    file_name=os.path.join(dir,name)
    CSVtoTSV(file_name)