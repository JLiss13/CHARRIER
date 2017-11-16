# Automate the merging of .csv files into one large .csv file
# For more information on how I created the script please visit my github account
import pandas as pd
import os
import chardet
import time

def Convert12hr_to_24hour(dataframe1,headerindex):
    tempvar=pd.to_datetime(dataframe1[headerindex], errors="coerce")
    tempvar=tempvar.dt.strftime('%m/%d/%y %H:%M:%S.%f')
    dataframe1[headerindex]=tempvar
    # dataframe1.index=datetime.strptime(dataframe1.index, "%m/%d/%y %I:%M:%S.%f %p").strftime("%m/%d/%y %H:%M:%S.%f")
    return dataframe1
def ConvertDecimalHours2TimestampwithMilliseconds(dir,filename):
    start_time = time.time()
    day=filename[11:19].replace('_','/')
    # dir = "/Users/Jaliss/Documents/NASA/C-HARRIER/C-HARRIER_DATA/OCEANIA_Aircraft_Data_11_05_2013/"

    #10 Hz data
    file=os.path.join(dir,filename) # 10 Hz aircraft data csv file
    tempcsvarray = pd.read_csv(file)
    print("Size of the tempcsvarray: " + str(tempcsvarray.shape))
    headers=tempcsvarray.dtypes.index
    rec_array=[]
    rec_temp_array=pd.DataFrame(columns=['DateTimeUTC'])
    # rec_array=pd.DataFrame(columns=headers)
    UTCtime = tempcsvarray['UTC time (HH.hhhhh)']
    print(UTCtime.shape)
    for i in range(1,tempcsvarray.shape[0]):
        hours = int(UTCtime[i])
        minutes = int((UTCtime[i] * 60) % 60)
        seconds = int((UTCtime[i] * 3600) % 60)
        ms = int((UTCtime[i] * 3600000) % 1000)
        ns = int((UTCtime[i] * 12960000) % 60) # Just in case we want to use nanosecond accuracy
        # ms = int(round((UTCtime[i] * 3600000) % 1000))
        string = day + ' ' + str(hours).zfill(2) + ':' + str(minutes).zfill(2)+ ':' + str(seconds).zfill(2) + '.'+ str(ms).zfill(3)
        rec_array.append(string)
        print(string)
    rec_temp_array['DateTimeUTC']=rec_array
    print(rec_temp_array.shape)
    tempcsvarray.insert(1,'DateTimeUTC', rec_temp_array)
    tempcsvarray.columns= pd.Series(tempcsvarray.columns).str.replace('_x','') #Make 1 Hz and 10 Hz match
    tempcsvarray.to_csv(file.replace('.TXT','')+'_'+ "Modified"+".csv", sep=',')
    print("Done with converting HH.hhhhh to BSI timestamps")

def MergeBSIdataCAPS(dir,dayofflight):
    start_time = time.time()
    codedir=os.getcwd() #Grab current code directory and return to after code is run
    # dir=input("What is the root directory where the cabin csv files exist?")
    # dir="/Users/Jaliss/Documents/NASA/C-HARRIER/C-HARRIER_DATA/OCEANIA_Aircraft_Data_11_05_2013/"
    # dir='/Users/Jaliss/Documents/NASA/C-HARRIER/Deployment_Mission/9-5-17/BSI/C-AERO'
    os.chdir(dir)
    tempstr=dayofflight.replace('/','_')
    datadirectory='today'+ tempstr[8:10]+tempstr[0:2]+tempstr[3:5]
    # datadirectory=input("What is the name of directory where the cabin csv files exist? (i.e. 'today170911')")
    # dayofflight=input("What is the day of the flight? (i.e. '10/24/2013')")
    CAPS_SUFFIX=input("What is the CAPS data type you are merging? (i.e. URC, URE, URU)")
    # dayofflight='09/05/2017'
    folderlist=os.listdir(dir)
    folderlist = filter(lambda k: not '.' in k, folderlist)
    folderlist = filter(lambda k: not 'outputs' in k, folderlist)
    folderlist = filter(lambda k: not '_HOST_' in k, folderlist)
    folderlist = list(filter (lambda k: datadirectory in k, folderlist))
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
            files = filter(lambda k: CAPS_SUFFIX in k,files)
            files = filter(lambda k: not "._" in k,files) # Do not merge hidden files
        # files = filter(lambda k: k[0:2] == prefix in k, files) # filters out only files with the prefix beginning
            files = filter(lambda k: os.path.getsize(k) > 410, files) # Filter out all files larger than 410 bytes
            os.chdir(root)
            files = list(files)
            print(files)
            # filesmain = filter(lambda k: not 'Aux' in k, files)
            filesmain = list(files)
            with open(os.path.join(root, files[0]), 'rb') as f: #Determine encoding
                result = chardet.detect(f.read())  # or readline if the file is large
            csvarray = pd.read_csv(os.path.join(root, files[0]),encoding=result['encoding'])
            sizefilesarray=len(filesmain)
            for i in range(1,sizefilesarray):
                filename=filesmain[i]
                tempcsvarray = pd.read_csv(os.path.join(root, filename), encoding=result['encoding'])
                print(filename)
                if 'DateTimeUTC' in tempcsvarray.columns:
                    if len(tempcsvarray['DateTimeUTC'] ) > 0:
                        if dayofflight in str(tempcsvarray['DateTimeUTC'][0]).strip():
                            csvarray = csvarray.append(tempcsvarray)
                        # Append the new dataset to the preexisting within the directory
                            strday=dayofflight+" data"
                            print(strday)
                            print("Size of the tempcsvarray: " + str(tempcsvarray.shape))
                            print("Size of the csvarray: " + str(csvarray.shape))
                        else:
                            str_nodata="No more "+ dayofflight + " data"
                            print(str_nodata)
                            break
                    else:
                        str_empty = "File " + str(os.path.join(root, filename)) + " .csv is empty!!"
                        print(str_empty)
                else:
                    str_check="File " + str(os.path.join(root, filename))+" .csv needs headers to be checked!!"
                    print(str_check)
                    break
                    break
                    break
        nameofMergedBSIdata = "total_for_"+folder + CAPS_SUFFIX + ".csv"
        csvarray.to_csv(nameofMergedBSIdata, sep=',') #http://stackoverflow.com/questions/16923281/pandas-writing-dataframe-to-csv-file
        print("Printed " + nameofMergedBSIdata + "... ")
        print("Shape of " + nameofMergedBSIdata+ " is " + str(csvarray.shape))
    os.chdir(codedir)
    print("--- %s seconds ---" % (time.time() - start_time))
    return os.path.join(os.path.join(dir,datadirectory),nameofMergedBSIdata)

def MergeBSIdata(dir,dayofflight):
    start_time = time.time()
    codedir = os.getcwd()
    # dir=input("What is the root directory where the cabin csv files exist?")
    # dir="/Users/Jaliss/Documents/NASA/C-HARRIER/C-HARRIER_DATA/OCEANIA_Aircraft_Data_11_05_2013/"
    # dir='/Users/Jaliss/Documents/NASA/C-HARRIER/Deployment_Mission/9-5-17/BSI/C-AERO'
    os.chdir(dir)
    tempstr = dayofflight.replace('/', '_')
    datadirectory = 'today' + tempstr[8:10] + tempstr[0:2] + tempstr[3:5]
    # datadirectory=input("What is the data directory where the cabin csv files exist? (i.e. 'today')")
    # dayofflight='09/05/2017'
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
            print(files)
            filesmain = filter(lambda k: not 'Aux' in k, files)
            filesmain = list(filesmain)
            with open(os.path.join(root, files[0]), 'rb') as f:
                result = chardet.detect(f.read())  # or readline if the file is large
            csvarray = pd.read_csv(os.path.join(root, files[0]),encoding=result['encoding'])
            sizefilesarray=len(filesmain)
            for i in range(1,sizefilesarray):
                filename=filesmain[i]
                tempcsvarray = pd.read_csv(os.path.join(root, filename), encoding=result['encoding'])
                print(filename)
                if 'DateTimeUTC' in tempcsvarray.columns:
                    if len(tempcsvarray['DateTimeUTC'] ) > 0:
                        if dayofflight in str(tempcsvarray['DateTimeUTC'][0]).strip():
                            csvarray = csvarray.append(tempcsvarray)
                        # Append the new dataset to the preexisting within the directory
                            strday=dayofflight+" data"
                            print(strday)
                            print("Size of the tempcsvarray: " + str(tempcsvarray.shape))
                            print("Size of the csvarray: " + str(csvarray.shape))
                        else:
                            str_nodata="No more "+ dayofflight + " data"
                            print(str_nodata)
                            print("File number:" + str(i)+ "," + "Name: " + filename + ".Timestamp needs to be checked")
                            break
                    else:
                        str_empty = "File " + str(os.path.join(root, filename)) + " .csv is empty!!"
                        print(str_empty)
                else:
                    str_check="File " + str(os.path.join(root, filename))+" .csv needs headers to be checked!!"
                    print(str_check)
                    break
                    break
                    break
        nameofMergedBSIdata="total_for_"+folder+".csv"
        csvarray.to_csv(nameofMergedBSIdata, sep=',') #http://stackoverflow.com/questions/16923281/pandas-writing-dataframe-to-csv-file
        print("Printed " + nameofMergedBSIdata + "... ")
        print("Shape of " + nameofMergedBSIdata +  "is " + str(csvarray.shape))
    os.chdir(codedir)
    print("--- %s seconds ---" % (time.time() - start_time))
    return os.path.join(os.path.join(dir,datadirectory),nameofMergedBSIdata)