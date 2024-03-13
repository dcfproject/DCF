import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

df = np.loadtxt("C:/Users/Konrad/Desktop/DCF/Data/Yield/YieldData_1799_amended.txt")
energyData = df[:,0]
yieldData = df[:,1]
yerror = df[:,2]

X,Y = zip(*sorted(zip(energyData,yieldData)))

def arcTan(x, A, B, C, D):
    val = A*np.arctan(B*(x+C)) + D
    return val

guess632 = [10, 1, -650, 10]
guess992 = [40, 0.1, -1000, 50]
guess1213 = [10, 1, -1246, 10]
guess1587 = [15, 1, -1630, 15]
guess1799 = [20, 1, -1850, 25]

parameters, covariance = curve_fit(arcTan, X, Y,sigma=yerror, p0 = guess1799)
error = np.sqrt(np.diag(covariance))
f = open("C:/Users/Konrad/Desktop/DCF/Data/Yield/TotalYield_amended.txt", "a")
#f.write("{} {} \n".format(abs(parameters[2]), error[2]))
f.close
fitTan = arcTan(X, *parameters)
print(abs(parameters[2]), error[2])
plt.plot(X, Y, 'o', label='data')
plt.plot(X, fitTan, '-', label='arctan')
plt.axvline(x=abs(parameters[2]), color='red', linestyle='--', label='Resonance')
plt.errorbar(X, Y, yerr=yerror, fmt="none")
plt.legend()
plt.xlabel("TV + EV - Bias (kV)")
plt.ylabel("Yield (a.u.)")
plt.title("Yield vs Accelerator Parameters for second resonance at 992 keV")
plt.show()

