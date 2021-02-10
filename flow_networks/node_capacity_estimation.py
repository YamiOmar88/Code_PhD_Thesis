# Code for PhD Thesis - Flow networks (node capacity estimation)
# Data: train_date.csv
# Yamila Mariel Omar
# Date of original code: 9th February 2021
# Date of code last modification: 9th February 2021


import re
import json

# =============================================================================
# FUNCTION DEFINITIONS
# =============================================================================
def kadane_algorithm(A):
    i, thisSum, maxSum = 0, 0, 0
    startIndex, endIndex = 0, -1
    for j in range(len(A)):
        thisSum = thisSum + A[j]
        if thisSum > maxSum:
            maxSum = thisSum
            startIndex = i
            endIndex   = j
        elif thisSum < 0:
            thisSum = 0
            i = j + 1
    return (maxSum, startIndex, endIndex)



# =============================================================================
# MAIN
# =============================================================================
if __name__ == "__main__":
    # =========================================
    # Process train_date.csv
    # =========================================
    filename = "/home/ubadmin/PhD/CET_4/code/data/train_date.csv"
    print("Processing: ", filename, "\n")

    first_line = True
    t_i = {} # stations initial time-stamp values
    with open(filename, "r") as f:
        for row in f:
            # Save column names
            if first_line:
                column_names = row.strip().split(",")
                del column_names[0]
                first_line = False
                continue

            row = row.strip().split(",")
            id = int(row.pop(0))    # "Id"

            # Remove NA
            empty_string_list = ["" == i for i in row]
            columns_to_keep = [i for (i, v) in zip(column_names, empty_string_list) if not v]
            row = filter(None, row)

            # Make time-stamp values float
            row = [float(i) for i in row]

            # For each processed item, save the initial time-stamp value
            # at each visited workstation
            vStat = list(set(re.findall("L._(S.+?)_D", " ".join(columns_to_keep))))
            for s in vStat:
                c = [s in i for i in columns_to_keep]
                sensorData = [v for (i,v) in zip(c,row) if i]
                sensorData = set(sensorData)
                t_i[s] = t_i.get(s, [])
                t_i[s].append( min(sensorData) )

    print("Finished processing file: ", filename, "\n")

    # Save intermediate results
    with open("results/time_stamps_at_each_workstation.json", "w") as f:
        json.dump(t_i, f, sort_keys=True, indent=4)


    # =========================================
    # Make change array
    # =========================================
    print("Proceeding to calculate the change arrays.")
    all_change_arrays = dict()
    time = [x* 0.01 for x in range(171849)]
    for k,v in t_i.items():
         # Make dictionary with time values as keys and number of occurrences as values
        time_stamp_frequency = {}
        for ts in v:
            time_stamp_frequency[ts] = time_stamp_frequency.get(ts, 0) + 1

        # Make "change" array
        change_array = []
        for i in range(1, 171849, 1):
            c = time_stamp_frequency.get(time[i], 0) - time_stamp_frequency.get(time[i-1], 0)
            change_array.append(c)
        all_change_arrays[k] = change_array

    # Save intermediate results
    with open("results/change_arrays.json", "w") as f:
        json.dump(all_change_arrays, f, sort_keys=True, indent=4)

    # =========================================
    # Find maximum subarray
    # =========================================
    print("Proceeding to calculate the maximum subarrays.")
    maximum_subarray = dict()
    for k,v in all_change_arrays.items():
        s, idL, idR = kadane_algorithm(v)
        tL, tR = time[idL+1], time[idR+1]
        maximum_subarray[k] = {"maximum_sum": s, "left_time":tL, "right_time":tR}

    # Save intermediate results
    with open("results/maximum_subarray.json", "w") as f:
        json.dump(maximum_subarray, f, sort_keys=True, indent=4)

    # =========================================
    # Count number of elements processed in maximum subarray time
    # =========================================
    print("Counting number of units processed in maximum subarray time.")
    units_processed = {}
    for k,v in t_i.items():
         # Make dictionary with time values as keys and number of occurrences as values
        time_stamp_frequency = {}
        for ts in v:
            time_stamp_frequency[ts] = time_stamp_frequency.get(ts, 0) + 1

        # Calculate Number of units processes in maxSum time lapse
        units = 0
        for kk,vv in time_stamp_frequency.items():
            if kk >= maximum_subarray[k]["left_time"] and kk <= maximum_subarray[k]["right_time"]:
                units = units + vv

        time_lapse = maximum_subarray[k]["right_time"] - maximum_subarray[k]["left_time"]
        capacity_estimation = units * (16.75 / 7) / time_lapse # in units/day
        capacity_estimation = int(round(capacity_estimation, 0))
        units_processed[k] = capacity_estimation

    # ============================================
    # SAVE RESULTS
    # ============================================
    with open("results/capacity_estimation.json", "w") as f:
        json.dump(units_processed, f, sort_keys=True, indent=4)
