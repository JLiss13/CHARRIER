import pandas as pd
import time
import matplotlib.pyplot as plt
#Convert the HH.hhhhhhh timestamp to mm/ddd/yyyy HH:MM:SS
start_time = time.time()
day='10/24/13 '
file="CABIN_10hz_13110505.TXT" # 1 or 10 Hz aircraft data csv file
tempcsvarray = pd.read_csv(file)
print("Size of the tempcsvarray: " + str(tempcsvarray.shape))
headers=tempcsvarray.dtypes.index
rec_array=[]
rec_temp_array=pd.DataFrame(columns=['DateTimeUTC'])
# rec_array=pd.DataFrame(columns=headers)
UTCtime = tempcsvarray['UTC (HH.hhhhhhh)']
for i in range(1,tempcsvarray.shape[0]):
    hours = int(UTCtime[i])
    minutes = int((UTCtime[i] * 60) % 60)
    seconds = int((UTCtime[i] * 3600) % 60)
    ms = int((UTCtime[i] * 216000) % 60)
    ns = int((UTCtime[i] * 12960000) % 60) # Just in case we want to use nanosecond accuracy
    # ms = int(round((UTCtime[i] * 3600000) % 1000))
    string = day + str(hours).zfill(2) + ':' + str(minutes).zfill(2)+ ':' + str(seconds).zfill(2) + ':'+ str(ms).zfill(2)
    rec_array.append(string)
    print(string)
rec_temp_array['DateTimeUTC']=rec_array
tempcsvarray.insert(1,'DateTimeUTC', rec_temp_array)
tempcsvarray.to_csv("Modified"+ file.replace('.TXT','')+'_'+ ".csv", sep=',')
print("--- Program took %s seconds ---" % (time.time() - start_time))