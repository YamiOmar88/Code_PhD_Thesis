# Code for PhD Thesis - Flow networks plots
# Data: time_stamps_at_each_workstation.json and change_arrays.json
# Yamila Mariel Omar
# Date of original code: 25th March 2021
# Date of code last modification: 25th March 2021


import json
import matplotlib.pyplot as plt

# =============================================================================
# PLOT - UNITS PROCESSED PER TIME STAMP
# =============================================================================
time_stamps = open("results/time_stamps_at_each_workstation.json")
time_stamps = json.load(time_stamps)

S0 = dict()
for ts in time_stamps["S0"]:
    S0[ts] = S0.get(ts, 0) + 1

x = list(S0.keys())
x.sort()
y = [S0.get(i, 0) for i in x]


plt.bar(x[:80], y[:80], width=0.01, color="#646464")
plt.xlabel("anonymized time-stamp")
plt.ylabel("# of units processed")
plt.savefig("results/capacity_estimation_v0_1.pdf")
plt.close()


# =============================================================================
# PLOT - CHANGE ARRAY
# =============================================================================
change_arrays = open("results/change_arrays.json")
change_arrays = json.load(change_arrays)

plt.bar(x[:80], change_arrays["S0"][:80], width=0.01, color="#646464")
plt.xlabel("anonymized time-stamp")
plt.ylabel("change in units processed")
plt.savefig("results/capacity_estimation_v0_2.pdf")
plt.close()
