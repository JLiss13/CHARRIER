import pandas as pd
import time
import os
import numpy as np
#Linear interpolation
start_time = time.time()
dir="/Users/Jaliss/Documents/NASA/C-HARRIER/C-HARRIER_DATA/OCEANIA_Aircraft_Data_11_05_2013/TO_Cabin_Data_11_5_2013"
file=os.path.join(dir,"ModifiedCABIN_10hz_13110505_.csv") # 1 or 10 Hz aircraft data csv file
tempcsvarray = pd.read_csv(file)
print("Size of the tempcsvarray: " + str(tempcsvarray.shape))
headers=tempcsvarray.dtypes.index
tempcsvarray_large=pd.DataFrame(columns = headers, index=[list(np.arange(0,tempcsvarray.shape[0],0.25))])
# tempcsvarray_large=tempcsvarray_large.merge(tempcsvarray, left_index=True, right_index=True, how = "outer")
tempcsvarray=tempcsvarray.merge(tempcsvarray_large, left_index=True, right_index=True, how = "outer")





print("--- Program took %s seconds ---" % (time.time() - start_time))