import numpy as np
import matplotlib.pyplot as plt

df = np.loadtxt("C:/Users/Konrad/Desktop/DCF/DCF/Data/Yield/YieldData_Stability.txt")
yieldData = df[:,1]
yerror = df[:,2]
xData = np.arange(2,2*(len(yieldData)+1),2)

plt.plot(xData, yieldData, 'o', label='data', color = "blue", markersize = 4)
plt.errorbar(xData, yieldData, yerr=yerror, color = "blue", fmt="none", capsize = 3, capthick = 1, elinewidth = 1)
plt.xlabel("Time (min)", fontsize = 12)
plt.ylabel("Yield (a.u.)", fontsize = 12)
plt.show()


