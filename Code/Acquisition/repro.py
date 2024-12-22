import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

df = np.loadtxt("C:/Users/Konrad/Desktop/DCF/DCF/Data/Yield/YieldData_992.txt")
energyData = df[:,0]
yieldData = df[:,1]
yerror = df[:,2]

model = np.loadtxt("C:/Users/Konrad/Desktop/DCF/DCF/Data/Yield/Model/992.txt")
x = model[:,0]
y = model[:,1]

df2 = np.loadtxt("C:/Users/Konrad/Desktop/DCF/DCF/Data/Yield/YieldData_992_II.txt")
energyData2 = df2[:,0]
yieldData2 = df2[:,1]
yerror2 = df2[:,2]

model2 = np.loadtxt("C:/Users/Konrad/Desktop/DCF/DCF/Data/Yield/Model/992_II.txt")
x2 = model2[:,0]
y2 = model2[:,1]

X,Y, Yerror = zip(*sorted(zip(energyData,yieldData,yerror)))
X2,Y2, Y2error = zip(*sorted(zip(energyData2,yieldData2,yerror2)))

plt.plot(X, Y, 'o', markersize = 5, color = "red", label='First 992 keV scan') 
plt.errorbar(X, Y, yerr=Yerror, color = "red", fmt="none", capsize = 3, capthick = 1, elinewidth = 1)
plt.plot(X2, Y2, 'o', markersize = 5, color = "blue", label='Second 992 keV scan') 
plt.errorbar(X2, Y2, yerr=Y2error, color = "blue", fmt="none", capsize = 3, capthick = 1, elinewidth = 1)
plt.minorticks_on()
plt.xlabel("TV + EV - Bias (kV)", fontsize=23)
plt.ylabel("Yield (a.u.)", fontsize=23)
plt.xticks( fontsize = 16) 
plt.yticks(fontsize = 16)
plt.plot(x, y, color = "red")
plt.plot(x2, y2, color = "blue")
plt.legend(frameon = False, fontsize = 14)
plt.tight_layout()
plt.gcf().set_size_inches(6, 5)
plt.savefig("C:/Users/Konrad/Desktop/repro.png", dpi=1200)
plt.show()
