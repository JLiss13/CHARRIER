import pandas as pd
import time
import os
from datetime import datetime
import numpy as np

#Linear interpolation
start_time = time.time()
dir="/Users/Jaliss/Documents/NASA/C-HARRIER/C-HARRIER_DATA/OCEANIA_Aircraft_Data_11_05_2013"
fileaircraft10=os.path.join(dir,"TO_Cabin_Data_11_5_2013/CABIN_10hz_13110505_Modified.csv") # 10 Hz aircraft data csv file
fileaircraft1=os.path.join(dir,"TO_Cabin_Data_11_5_2013/CABIN_1hz_v2_13110505_Modified.csv") # 10 Hz aircraft data csv file
fileBSI=os.path.join(dir,"CAIR_Data_11_5_2013/CAIR_Data_11_5_2013.csv") # BSI file data with millisecond resolution
print("Ready to input data")
dtypes = [datetime, str, float]

#Bring in aircraft data 10 Hz
tempcsvarraypre10 = pd.read_csv(fileaircraft10)
tempcsvarray10=tempcsvarraypre10
print("Done uploading 10 Hz aircraft data")

#Bring in aircraft data 1 Hz
# tempcsvarraypre1 = pd.read_csv(fileaircraft1)
# tempcsvarray1=tempcsvarraypre1
# tempcsvarray1timestamps=tempcsvarray1['DateTimeUTC']
# print("Done uploading 1 Hz aircraft data")

#Bring in BSI data 15 Hz
tempcsvarrayBSI = pd.read_csv(fileBSI)
print("Done uploading BSI data")
print("Size of the BSI Data: " + str(tempcsvarrayBSI.shape))

#Sets the index
tempcsvarray10.set_index('DateTimeUTC', inplace=True)
# tempcsvarray1.set_index('DateTimeUTC', inplace=True)
# tempcsvarray1timestamps.set_index('DateTimeUTC', inplace=True)
tempcsvarrayBSI.set_index('DateTimeUTC', inplace=True)

#Convert into ms units
tempcsvarray10.index = pd.to_datetime(tempcsvarray10.index, format="%m/%d/%Y %H:%M:%S.%f")
# tempcsvarray1.index = pd.to_datetime(tempcsvarray1.index, format="%m/%d/%Y %H:%M:%S.%f")
# tempcsvarray1timestamps.index = pd.to_datetime(tempcsvarray1timestamps.index, format="%m/%d/%Y %H:%M:%S.%f")
tempcsvarrayBSI.index = pd.to_datetime(tempcsvarrayBSI.index, format="%m/%d/%Y %H:%M:%S.%f")


# Merges the union between the two datasets and does not delete any preexisting data from either
# tempcsvarraylarge10a1=tempcsvarray10.merge(tempcsvarray1timestamps, left_index=True, right_index=True, how = "outer")
# print("Size of the merged 10Hz with 1 Hz Timestamps: " + str(tempcsvarraylarge10a1.shape))
# tempcsvarraylarge10a1=tempcsvarray10.merge(tempcsvarray1, left_index=True, right_index=True, how = "outer")
# print("Size of the merged 10Hz data with 1 Hz data: " + str(tempcsvarraylarge10a1.shape))
# tempcsvarraylarge10a1[50:1000][:].to_csv("Snapshot_of_MergedData_10Hz_and_1Hz"+".csv", sep=',')
tempcsvarraylarge=tempcsvarray10.merge(tempcsvarrayBSI, left_index=True, right_index=True, how = "outer")
tempcsvarraylargematches=tempcsvarray10.merge(tempcsvarrayBSI, left_index=True, right_index=True, how = "inner")
# print("Size of the matching aircraft data with BSI data: " + str(tempcsvarraylarge.shape))

# remove all NaT values
tempcsvarraylarge["TMP"] = tempcsvarraylarge.index.values                # index is a DateTimeIndex
tempcsvarraylarge = tempcsvarraylarge[tempcsvarraylarge.TMP.notnull()] # remove all NaT values
tempcsvarraylarge.drop(["TMP"], axis=1, inplace=True)                    # delete TMP again

#Make files
print("Size of the merged 10Hz Hz aircraft data with the BSI data at 15 Hz: " + str(tempcsvarraylarge.shape))
print("Making merged files")
tempcsvarraylarge.to_csv("Big_Kahuna"+".csv", sep=',')
tempcsvarraylargematches.to_csv("TotalMatchesBig_Kahuna"+".csv", sep=',')

#Perform interpolation
print('Performing Interpolation')
tempcsvarrayintpol=tempcsvarraylarge.interpolate(method='time')
print("Making interpolated files")
tempcsvarrayintpol.to_csv("Big_Kahuna_with_Lin_intpol"+".csv", sep=',')

#Created snapshot of interpolated data
shorttempcsvarrayintpol=tempcsvarrayintpol[50:1000][:]
shorttempcsvarrayintpol.to_csv("Small_Kahuna_with_Lin_intpol"+".csv", sep=',')

#Print out performance time
print("--- Program took %s seconds ---" % (time.time() - start_time))