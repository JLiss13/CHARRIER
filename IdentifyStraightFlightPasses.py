import pandas as pd
import time
import matplotlib.pyplot as plt
#Objective of Code: Determine the straight passes of the flight trajectories. An output file with timestamps
#of the start and end along with their associated data will be saved into the current directory.
start_time = time.time()
file="CABIN_10hz_13110505.TXT" # 1 or 10 Hz aircraft data csv file
tempcsvarray = pd.read_csv(file)
print("Size of the tempcsvarray: " + str(tempcsvarray.shape))
options='1'
headers=tempcsvarray.dtypes.index
rec_array=pd.DataFrame(columns=headers)
rec_array_2=pd.DataFrame(columns=headers)
#Convert the HH.hhhhhhh timestamp to mm/ddd/yyyy HH:MM:SS
exclude_threshold=3 # delta degrees
include_threshold=0.2 # delta degrees
if options == '1': #Plot Time vs Heading
    plt.figure()
    plt.plot(tempcsvarray['UTC (HH.hhhhhhh)'],tempcsvarray['Heading (deg)'],'.')
    plt.xlabel('UTC (HH.hhhhhhh)')
    plt.ylabel('Heading (deg)')
    plt.title('UTC (HH.hhhhhhh) vs Heading (deg)')
    plt.savefig('Allflightrecords.png')

elif options == '2': # Check when the heading changes indicate beginning and end of turns
    print("I'm in option 2 baby")
    pre_head=tempcsvarray['Heading (deg)'][1]
    for i in range(9,tempcsvarray.shape[0],10):
        cur_head=tempcsvarray['Heading (deg)'][i]
        if abs(pre_head-cur_head) > exclude_threshold:
            rec_array = rec_array.append(tempcsvarray.ix[i,:])
        pre_head=cur_head
    rec_array.to_csv("Recorded_Array_of_flight_turns.csv", sep=',')
    plt.figure()
    plt.plot(rec_array['UTC (HH.hhhhhhh)'],rec_array['Heading (deg)'],'*')
    plt.xlabel('UTC (HH.hhhhhhh)')
    plt.ylabel('Heading (deg)')
    plt.title('UTC (HH.hhhhhhh) vs Heading (deg)')
    # plt.show()
    plt.savefig('Turn_Flight_Paths.png')
elif options == '3': # Check when the straight flight paths occur
    print("I'm in option 3 baby")
    pre_head=tempcsvarray['Heading (deg)'][1]
    ##Filter to find all straight paths
    print("Start of filter 1")
    for i in range(1,tempcsvarray.shape[0],3):
        cur_head=tempcsvarray['Heading (deg)'][i]
        if abs(pre_head-cur_head) < include_threshold:
            rec_array = rec_array.append(tempcsvarray.ix[i,:])
        pre_head=cur_head
    rec_array.to_csv("Recorded_Array_of_flight_straights.csv", sep=',')
    print("Done with filter 1")
    ##Filter to clean up data for plotting
    pre_head_2 = rec_array['Heading (deg)'][1]
    plt.figure()
    plt.plot(rec_array['UTC (HH.hhhhhhh)'],rec_array['Heading (deg)'],'*')
    plt.xlabel('UTC (HH.hhhhhhh)')
    plt.ylabel('Heading (deg)')
    plt.title('UTC (HH.hhhhhhh) vs Heading (deg)')
    plt.savefig('Straight_Flight_Paths.png')
    # plt.show()
    print("Start of filter 2")
    row_iterator = rec_array.iterrows()
    # for i in range(1,rec_array.shape[0]):
    #     cur_head_2 = rec_array['Heading (deg)'][i]
    #     if abs(pre_head_2 - cur_head_2) > exclude_threshold:
    #         print(rec_array.ix[i,:])
    #         rec_array_2 = rec_array_2.append(rec_array.ix[i,:])
    #     pre_head_2 = cur_head_2
    for index,row in row_iterator:
        cur_head_2 = row['Heading (deg)']
        if abs(pre_head_2 - cur_head_2) > exclude_threshold:
            print(row)
            rec_array_2 = rec_array_2.append(row)
        pre_head_2 = cur_head_2
    print("Done with filter 2")
    rec_array.to_csv("Recorded_Array_of_flight_straights_start_end.csv", sep=',')
    plt.figure()
    plt.plot(rec_array_2['UTC (HH.hhhhhhh)'],rec_array_2['Heading (deg)'],'*')
    plt.xlabel('UTC (HH.hhhhhhh)')
    plt.ylabel('Heading (deg)')
    plt.title('UTC (HH.hhhhhhh) vs Heading (deg)')
    # plt.show()
    plt.savefig('Straight_Flight_Paths_start_end.png')
print("--- Program took %s seconds ---" % (time.time() - start_time))