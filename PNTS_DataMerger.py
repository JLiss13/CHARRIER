import pandas as pd
import time
import os
from datetime import datetime
import PNT_Library as PNT
import sys

#Bring in data
start_time = time.time()
codedir=os.getcwd()
# dir="/Users/Jaliss/Documents/NASA/C-HARRIER/C-HARRIER_DATA/OCEANIA_Aircraft_Data_11_05_2013"
dayofflight = input("What is the day of the flight? (i.e. '09/05/2017')")
aircraftdir = input('What is the data directory with all the aircraft data? (i.e. [Path Directory ]/AircraftData)')
# fileaircraft10=os.path.join(dir,"TO_Cabin_Data_11_5_2013/CABIN_10hz_13110505_Modified.csv") # 10 Hz aircraft data csv file
aircraftdata_list=os.listdir(aircraftdir)
tempstr=str(dayofflight.replace('/','_').replace('20',''))
aircraftdata_list=filter(lambda k: tempstr in k, aircraftdata_list)
aircraftdata_list=filter(lambda k: '.TXT' in k,aircraftdata_list)
aircraftdata_list=filter(lambda k: not '._' in k,aircraftdata_list)
fileaircraft10=list(aircraftdata_list)
if len(fileaircraft10) == 0:
    print('There is not aircraft data for that particular day. Please check aircraft data directory.')
    sys.exit()
fileaircraft10=fileaircraft10[0]

# fileaircraft10=input('What is the name of the modified 10Hz aircraft data? (i.e. CABIN_10hz_09_05_17_050.txt')
PNT.ConvertDecimalHours2TimestampwithMilliseconds(aircraftdir,fileaircraft10)

# Merge BSI data and output path to the file
BSIdir=input('What is the BSI day data directory? (i.e. [Path Directory]/C-AERO)')
FileUniqueSuffix=os.path.split(BSIdir)[1]+"_"+fileaircraft10[11:19]
if 'CAPS' in BSIdir:
    fileBSI=PNT.MergeBSIdataCAPS(BSIdir, dayofflight)
else:
    fileBSI=PNT.MergeBSIdata(BSIdir,dayofflight)

print("Ready to input data")
dtypes = [datetime, str, float]

#Bring in modified aircraft data 10 Hz
print("Begin uploading aircraft data")
fileaircraft10_mod=fileaircraft10.replace('.TXT','_Modified.csv')
tempcsvarraypre10 = pd.read_csv(os.path.join(aircraftdir,fileaircraft10_mod))
tempcsvarray10=tempcsvarraypre10
print("Done uploading 10 Hz aircraft data")

#Bring in BSI data at 15 Hz
print("Begin uploading BSI data")
tempcsvarrayBSI = pd.read_csv(os.path.join(BSIdir,fileBSI))
#Convert all BSI 12 hour time data to 24 hour time data
tempvar=pd.to_datetime(tempcsvarrayBSI['DateTimeUTC'], errors="coerce")
tempvar=tempvar.dt.strftime('%m/%d/%y %H:%M:%S.%f')
tempcsvarrayBSI['DateTimeUTC']=tempvar

print("Done uploading BSI data")
print("Size of the BSI Data: " + str(tempcsvarrayBSI.shape))

#Sets the index
tempcsvarray10.set_index('DateTimeUTC', inplace=True)
tempcsvarrayBSI.set_index('DateTimeUTC', inplace=True)

#Convert into ms units
tempcsvarray10.index = pd.to_datetime(tempcsvarray10.index, format="%m/%d/%y %H:%M:%S.%f")
tempcsvarrayBSI.index = pd.to_datetime(tempcsvarrayBSI.index, format="%m/%d/%y %H:%M:%S.%f")

print("Performing timestamp synchronization")
# Merges the union between the two datasets and does not delete any preexisting data from either
tempcsvarraylarge=tempcsvarray10.merge(tempcsvarrayBSI, left_index=True, right_index=True, how = "outer")
tempcsvarraylargematches=tempcsvarray10.merge(tempcsvarrayBSI, left_index=True, right_index=True, how = "inner")
print("Done performing timestamp synchronization")

print("Removing NaN timestamps from data")
# remove all NaT values
tempcsvarraylarge["TMP"] = tempcsvarraylarge.index.values                # index is a DateTimeIndex
tempcsvarraylarge = tempcsvarraylarge[tempcsvarraylarge.TMP.notnull()] # remove all NaT DateTimeIndex_values
tempcsvarraylarge.drop(["TMP"], axis=1, inplace=True)                    # delete TMP again
print("Done removing NaN Timestamps data")

#Make files
print("Size of the merged 10Hz Hz aircraft data with the BSI data at 15 Hz: " + str(tempcsvarraylarge.shape))
print("Making merged files")
if not os.path.exists(os.path.join(BSIdir,"MergedFiles")):
    os.makedirs(os.path.join(BSIdir,"MergedFiles/"))
tempcsvarraylarge.to_csv(os.path.join(BSIdir,"MergedFiles/"+"Merged_BSI_Aircraft_data"+FileUniqueSuffix+".csv"), sep=',')
tempcsvarraylarge.to_csv(os.path.join(BSIdir,"MergedFiles/"+"Merged_BSI_Aircraft_data"+FileUniqueSuffix+".tsv"), sep='\t')
tempcsvarraylargematches.to_csv(os.path.join(BSIdir,"MergedFiles/"+"Merged_BSI_Aircraft_data_time_matches"+FileUniqueSuffix+".csv"), sep=',')
tempcsvarraylargematches.to_csv(os.path.join(BSIdir,"MergedFiles/"+"Merged_BSI_Aircraft_data_time_matches"+FileUniqueSuffix+".tsv"), sep='\t')

print("Done making timestamp synchronized merged file")

#Performing flag to show which aircraft data was intepolated
Raw_Data_Flag=tempcsvarraylarge.iloc[:, 4] > 0
tempcsvarraylarge['Original_Untainted_Aircraft_Data_Flag']=Raw_Data_Flag

# #Performing flag to show which BSI radiometer data was linearly intepolated
# Raw_Data_Flag=tempcsvarraylarge.iloc[:, 32] > 0
# tempcsvarraylarge['Original_BSI_Data_Flag']=Raw_Data_Flag

#Perform interpolation only on the first 30 columns all radiometer data is untouched
aircraftheaderlist=list(tempcsvarray10)
print('Performing Interpolation on aircraft data only. All radiometer data is untouched.')
tempcsvarraylargecopy=tempcsvarraylarge
tempcsvarrayintpoltemp=tempcsvarraylargecopy.iloc[:,:30] #https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.pop.html
tempcsvarrayintpoltemp=tempcsvarrayintpoltemp.interpolate(method='time') #https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.interpolate.html
tempcsvarrayintpol=pd.concat([tempcsvarrayintpoltemp, tempcsvarraylarge.iloc[:,30:]], axis=1) #https://pandas.pydata.org/pandas-docs/stable/merging.html
print('Done performing Interpolation')
print("Making interpolated files")
tempcsvarrayintpol.to_csv(os.path.join(BSIdir,"MergedFiles/"+"Merged_BSI_Aircraft_data_with_Lin_intpol"+FileUniqueSuffix+".csv"), sep=',')
tempcsvarrayintpol.to_csv(os.path.join(BSIdir,"MergedFiles/"+"Merged_BSI_Aircraft_data_with_Lin_intpol"+FileUniqueSuffix+".tsv"), sep='\t')

#Created snapshot of interpolated data
shorttempcsvarrayintpol=tempcsvarrayintpol[50000:60000][:]
shorttempcsvarrayintpol.to_csv(os.path.join(BSIdir,"MergedFiles/"+"Snapshot_of_Merged_BSI_Aircraft_data_with_Lin_intpol"+FileUniqueSuffix+".csv"), sep=',')
shorttempcsvarrayintpol.to_csv(os.path.join(BSIdir,"MergedFiles/"+"Snapshot_of_Merged_BSI_Aircraft_data_with_Lin_intpol"+FileUniqueSuffix+".tsv"), sep='\t')

#Print out performance time
os.chdir(codedir)
print("--- Program took %s seconds ---" % (time.time() - start_time))