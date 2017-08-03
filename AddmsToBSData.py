import pandas as pd
import time
import os
#Convert the HH.hhhhhhh timestamp to mm/ddd/yyyy HH:MM:SS
start_time = time.time()
dir="/Users/Jaliss/Documents/NASA/C-HARRIER/C-HARRIER_DATA/OCEANIA_Aircraft_Data_11_05_2013/CAIR_Data_11_5_2013"
os.chdir(dir)
datafile='297182106.csv'
# datafile='CAIR_Data_11_5_2013.csv'
tempcsvarray = pd.read_csv(datafile)
estruntime=tempcsvarray.shape[0]*0.00038871279629794033
print('Estimated runtime: '+ str(estruntime) + ' seconds')

print("Size of the tempcsvarray: " + str(tempcsvarray.shape))
MacroTimeStamp=tempcsvarray['DateTimeUTC']
MicroTimeStamp=tempcsvarray['Master_Time'] # 15 Hz data acquistion for all CAIR data
NewTimeStamp=[]
rec_temp_array=pd.DataFrame(columns=['ComboDateTimeUTC'])
for i in range(1,tempcsvarray.shape[0]):
    # seconds = int(MicroTimeStamp[i] % 60)
    ms = int((MicroTimeStamp[i] * 216000) % 60) # Can't quite figure out with Master_Time is. What is it?
    string = str(MacroTimeStamp[i]) + ':' + str(ms).zfill(2)
    # string = str(MacroTimeStamp[i])+ ':' + str(seconds).zfill(2) + ':' + str(ms).zfill(2)
    NewTimeStamp.append(string)
    print(string)
rec_temp_array['ComboDateTimeUTC']=NewTimeStamp
tempcsvarray.insert(1,'ComboDateTimeUTC', rec_temp_array)
tempcsvarray.to_csv("Modified"+ datafile.replace('.csv','')+'_'+ ".csv", sep=',')
print("--- Program actually took %s seconds ---" % (time.time() - start_time))