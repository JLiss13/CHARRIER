import pandas as pd
import time
import os
#Objective: Convert the HH.hhhhhhh timestamp to mm/ddd/yyyy HH:MM:SS
start_time = time.time()
day='10/24/2013 '
dir = "/Users/Jaliss/Documents/NASA/C-HARRIER/C-HARRIER_DATA/OCEANIA_Aircraft_Data_11_05_2013/"

#10 Hz data
file=os.path.join(dir,"TO_Cabin_Data_11_5_2013/CABIN_10hz_13110505.TXT") # 10 Hz aircraft data csv file
tempcsvarray = pd.read_csv(file)
print("Size of the tempcsvarray: " + str(tempcsvarray.shape))
headers=tempcsvarray.dtypes.index
rec_array=[]
rec_temp_array=pd.DataFrame(columns=['DateTimeUTC'])
# rec_array=pd.DataFrame(columns=headers)
UTCtime = tempcsvarray['UTC (HH.hhhhhhh)']
print(UTCtime.shape)
for i in range(1,tempcsvarray.shape[0]):
    hours = int(UTCtime[i])
    minutes = int((UTCtime[i] * 60) % 60)
    seconds = int((UTCtime[i] * 3600) % 60)
    ms = int((UTCtime[i] * 3600000) % 1000)
    ns = int((UTCtime[i] * 12960000) % 60) # Just in case we want to use nanosecond accuracy
    # ms = int(round((UTCtime[i] * 3600000) % 1000))
    string = day + str(hours).zfill(2) + ':' + str(minutes).zfill(2)+ ':' + str(seconds).zfill(2) + '.'+ str(ms).zfill(3)
    rec_array.append(string)
    print(string)
rec_temp_array['DateTimeUTC']=rec_array
print(rec_temp_array.shape)
tempcsvarray.insert(1,'DateTimeUTC', rec_temp_array)
tempcsvarray.columns= pd.Series(tempcsvarray.columns).str.replace('_x','') #Make 1 Hz and 10 Hz match
tempcsvarray.to_csv(file.replace('.TXT','')+'_'+ "Modified"+".csv", sep=',')
print("Done with 10 Hz data")

#1 Hz data
file=os.path.join(dir,"TO_Cabin_Data_11_5_2013/CABIN_1hz_v2_13110505.TXT") # 1 or 10 Hz aircraft data csv file
tempcsvarray = pd.read_csv(file)
print("Size of the tempcsvarray: " + str(tempcsvarray.shape))
headers=tempcsvarray.dtypes.index
rec_array=[]
rec_temp_array=pd.DataFrame(columns=['DateTimeUTC'])
# rec_array=pd.DataFrame(columns=headers)
UTCtime = tempcsvarray['HH.hhhhhh (Hours)']
print(UTCtime.shape)
for i in range(1,tempcsvarray.shape[0]):
    hours = int(UTCtime[i])
    minutes = int((UTCtime[i] * 60) % 60)
    seconds = int((UTCtime[i] * 3600) % 60)
    ms = int((UTCtime[i] * 3600000) % 1000)
    ns = int((UTCtime[i] * 12960000) % 60) # Just in case we want to use nanosecond accuracy
    # ms = int(round((UTCtime[i] * 3600000) % 1000))
    string = day + str(hours).zfill(2) + ':' + str(minutes).zfill(2)+ ':' + str(seconds).zfill(2) + '.'+ str(ms).zfill(3)
    rec_array.append(string)
    print(string)
rec_temp_array['DateTimeUTC']=rec_array
print(rec_temp_array.shape)
tempcsvarray.insert(1,'DateTimeUTC', rec_temp_array)
tempcsvarray.columns= pd.Series(tempcsvarray.columns).str.replace('_y','') #Make 1 Hz and 10 Hz match
tempcsvarray.to_csv(file.replace('.TXT','')+'_'+ "Modified"+".csv", sep=',')
print("Done with 1 Hz data")

print("--- Program took %s seconds ---" % (time.time() - start_time))