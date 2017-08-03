import pandas as pd
import time
import matplotlib.pyplot as plt
#Perform Linear Interpolation on 10Hz Aircraft Data
start_time = time.time()
day='10/24/13 '
file="CABIN_10hz_13110505.TXT" # 1 or 10 Hz aircraft data csv file
tempcsvarray = pd.read_csv(file)
print("Size of the tempcsvarray: " + str(tempcsvarray.shape))
headers=tempcsvarray.dtypes.index
