# Automate the merging of .csv files into the xls format you want
# For more information on how I created the script please visit
# https://xlsxwriter.readthedocs.io/working_with_pandas.html or my github account
import os
import time
start_time = time.time()
import pandas as pd
# dir=input("What is the root directory where the cabin csv files exist?")
dir="/Users/Jaliss/Documents/NASA/C-HARRIER/C-HARRIER_DATA/OCEANIA_Aircraft_Data_11_05_2013/"
os.chdir(dir);
datadirectory='CAIR_Data_11_5_2013'
# finalfilename='comm_data_2017_02'
# Create a Pandas Excel writer using XlsxWriter as the engine.
# writer = pd.ExcelWriter(finalfilename + '.xlsx', engine='xlsxwriter')
folderlist=os.listdir(dir)
folderlist = filter(lambda k: not '.' in k, folderlist)
folderlist = filter(lambda k: not 'outputs' in k, folderlist)
folderlist = filter(lambda k: not '_HOST_' in k, folderlist)
folderlist = list(filter (lambda k: datadirectory in k, folderlist))
# prefix='29'; #Prefix to change
for folder in folderlist:
    print("Folder name " + folder + "--------------------------------------")
    for root, dirs, files in os.walk(os.path.join(dir,folder)):
    # On each iteration the files will be a list of files in the root directory
        files = filter(lambda k: not 'Log' in k, files)
        files = filter(lambda k: not '_HOST_' in k, files)
        files = filter(lambda k: '.csv' in k, files)
        files = filter(lambda k: not 'info' in k, files)
        files = filter(lambda k: not 'summary' in k, files)
        files = filter(lambda k: not folder in k,files)
        files = filter(lambda k: not 'Modified' in k, files)
    # files = filter(lambda k: k[0:2] == prefix in k, files) # filters out only files with the prefix beginning
        files = filter(lambda k: os.path.getsize(k) > 410, files) # Filter out all files larger than 410 bytes
        os.chdir(root)
        files = list(files)
        filesmain = filter(lambda k: not 'Aux' in k, files)
        filesmain = list(filesmain)
        filesaux = filter(lambda k: 'Aux' in k, files)
        filesaux = list(filesaux)
        #Obtains preexisting excel file or makes a new one using the first one as an example. It also takes notes of UnixTimeStamp column.
        csvarray = pd.read_csv(os.path.join(root, files[0]))
        tempcsvarrayAux = pd.read_csv(os.path.join(root, filesaux[0]))
        Milli = tempcsvarrayAux['Millisecond'].astype(str).str.zfill(3)
        csvarray['DateTimeUTC'] = csvarray['DateTimeUTC'] + '.'
        csvarray['DateTimeUTC'] = csvarray['DateTimeUTC'] + Milli
        # csvarray = pd.DataFrame(csvarray, columns=['DateTime', 'DateTimeUTC', 'Millisecond', 'Master_FrameNumber',
        #       'Master_Time','Master_Vin,Master_Iin','Master_Vchg','Master_Ichg','Master_Vbat','Master_Ibat','Master_Vp1'
        #       ,'Master_Ip1','Master_Vp2','Master_Ip2','Master_V33','Master_Temp','Es_FrameNumber','Es_Time','Es_Vin',
        #       'Es_Iin','Es_Temp','Es_Pressure','Li_FrameNumber','Li_Time','Li_Vin','Li_Iin','Li_Temp','Li_Pressure',
        #       'Lt_FrameNumber','Lt_Time','Lt_Vin','Lt_Iin','Lt_Temp','Lt_Pressure'])
        sizefilesarray=len(filesmain)
        # filename = filesmain[i]
        # tempcsvarray = pd.read_csv(os.path.join(root, filename))
        # while '10/24/2013' in str(csvarray['DateTimeUTC'][i]).strip():
        for i in range(1,sizefilesarray):
            filename=filesmain[i]
            filenameaux=filesaux[i]
            tempcsvarray = pd.read_csv(os.path.join(root, filename))
            tempcsvarrayAux = pd.read_csv(os.path.join(root, filenameaux))
            print(filename)
            if '10/24/2013' in str(tempcsvarray['DateTimeUTC'][i]).strip():
                Milli = tempcsvarrayAux['Millisecond'].astype(str).str.zfill(3)
                tempcsvarray['DateTimeUTC']=tempcsvarray['DateTimeUTC']+'.'
                tempcsvarray['DateTimeUTC']=tempcsvarray['DateTimeUTC']+ Milli
                csvarray = csvarray.append(tempcsvarray)
            # csvarray=csvarray.append(tempcsvarray,columns=['DateTime','DateTimeUTC','Millisecond','Master_FrameNumber',
            #     'Master_Time','Master_Vin,Master_Iin','Master_Vchg','Master_Ichg','Master_Vbat','Master_Ibat','Master_Vp1'
            #     ,'Master_Ip1','Master_Vp2','Master_Ip2','Master_V33','Master_Temp','Es_FrameNumber','Es_Time','Es_Vin',
            #     'Es_Iin','Es_Temp','Es_Pressure','Li_FrameNumber','Li_Time','Li_Vin','Li_Iin','Li_Temp','Li_Pressure',
            #     'Lt_FrameNumber','Lt_Time','Lt_Vin','Lt_Iin','Lt_Temp','Lt_Pressure'])
            # Append the new dataset to the preexisting within the directory
                print("10/24/2013 data")
                print("Size of the tempcsvarray: " + str(tempcsvarray.shape))
                print("Size of the csvarray: " + str(csvarray.shape))
            else:
                print("No more 10/24/2013 data")
                break
            print("--- %s seconds ---" % (time.time() - start_time))
    # print(type(csvarray)
    # csvarray['UnixTimeStamp'] = csvarray['UnixTimeStamp'].str.replace(':','') #http://stackoverflow.com/questions/14345739/replacing-part-of-string-in-python-pandas-dataframe
    # csvarray['UnixTimeStamp'] = csvarray['UnixTimeStamp'].replace(to_replace=':', value='', regex=True)
    # csvarray['DateTime'] = pd.to_datetime(csvarray['DateTime'], unit='s')
    # csvarray.drop(csvarray.columns[0]) #http://stackoverflow.com/questions/13411544/delete-column-from-pandas-dataframe
    csvarray.to_csv(folder+ ".csv", sep=',') #http://stackoverflow.com/questions/16923281/pandas-writing-dataframe-to-csv-file
    print("Printed " + folder+".csv ... ")
    print("Shape of " + folder+".csv is " + str(csvarray.shape))
os.chdir(dir);
print("--- %s seconds ---" % (time.time() - start_time))
# Close the Pandas Excel writer and output the Excel file.
# writer.save()
