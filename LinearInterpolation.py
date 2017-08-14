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
tempcsvarraypre10 = pd.read_csv(fileaircraft10)
tempcsvarray10=tempcsvarraypre10
print("Done uploading 10 Hz aircraft data")

tempcsvarraypre1 = pd.read_csv(fileaircraft1)
tempcsvarray1=tempcsvarraypre1
print("Done uploading 1 Hz aircraft data")

tempcsvarrayBSI = pd.read_csv(fileBSI)
print("Done uploading BSI data")
print("Size of the tempcsvarray: " + str(tempcsvarrayBSI.shape))

#Sets the index
tempcsvarray10.set_index('DateTimeUTC', inplace=True)
tempcsvarray1.set_index('DateTimeUTC', inplace=True)
tempcsvarrayBSI.set_index('DateTimeUTC', inplace=True)

#Convert into ms units
tempcsvarray10.index = pd.to_datetime(tempcsvarray10.index, format="%m/%d/%Y %H:%M:%S.%f")
tempcsvarray1.index = pd.to_datetime(tempcsvarray1.index, format="%m/%d/%Y %H:%M:%S.%f")
tempcsvarrayBSI.index = pd.to_datetime(tempcsvarrayBSI.index, format="%m/%d/%Y %H:%M:%S.%f")

# Merges the union between the two datasets and does not delete any preexisting data from either
tempcsvarraylarge10a1=tempcsvarray10.merge(tempcsvarray1, left_index=True, right_index=True, how = "outer")
tempcsvarraylarge=tempcsvarraylarge10a1.merge(tempcsvarrayBSI, left_index=True, right_index=True, how = "outer")
tempcsvarraylargematches=tempcsvarraylarge10a1.merge(tempcsvarrayBSI, left_index=True, right_index=True, how = "inner")

# remove all NaT values
tempcsvarraylarge["TMP"] = tempcsvarraylarge.index.values                # index is a DateTimeIndex
tempcsvarraylarge = tempcsvarraylarge[tempcsvarraylarge.TMP.notnull()] # remove all NaT values
tempcsvarraylarge.drop(["TMP"], axis=1, inplace=True)                    # delete TMP again

#Make files
print("Size of the tempcsvarraylarge: " + str(tempcsvarraylarge.shape))
print("Making merged files")
tempcsvarraylarge.to_csv("Big_Kahuna"+".csv", sep=',')
tempcsvarraylargematches.to_csv("TotalMatchesBig_Kahuna"+".csv", sep=',')

#Perform interpolation
print('Performing Interpolation')
tempcsvarrayintpol=tempcsvarraylarge.interpolate(method='time')
print("Making interpolated files")
tempcsvarrayintpol.to_csv("Big_Kahuna_with_Lin_intpol"+".csv", sep=',')

#Print out performance time
print("--- Program took %s seconds ---" % (time.time() - start_time))