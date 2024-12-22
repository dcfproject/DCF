import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

df = np.loadtxt("C:/Users/Konrad/Desktop/DCF/DCF/Data/Yield/Yield_binned/New/Yield_1799_am.txt")
energyData = df[:,0]
yieldData = df[:,1]
yerror = df[:,2]

color = ["blue", "green", "red", "black"]
run = df[:,3]
log = []
for i in run:
    log.append(color[int(i)])

df2 = np.loadtxt("C:/Users/Konrad/Desktop/DCF/DCF/Data/Yield/YieldData_992_II.txt")
energyData2 = df2[:,0]
yieldData2 = df2[:,1]
yerror2 = df2[:,2]


X,Y, Yerror, C = zip(*sorted(zip(energyData,yieldData,yerror,log)))
X2,Y2, Y2error = zip(*sorted(zip(energyData2,yieldData2,yerror2)))


def arcTan(x, A, B, C, D):
    val = A*np.arctan(B*(x+C)) + D
    return val

def targetWidth(x, H, resonance, width, dL, dR):
    f = H/((1+np.exp((resonance - x)/dL))*(1+np.exp((x - resonance - width)/dR)))
    return f

guess632 = [10, 1, -650, 10]
guess992 = [10, 0.1, -1000, 50]
guess992_II = [30, 0.2, -1018, 50]
guess1213 = [10, 1, -1246, 10]
guess1587 = [15, 1, -1630, 15]
guess1799 = [20, 3, -1850, 25]
guesswidth = [150, 1025, 10, 1, 1]


mode = "I"

#fit used to produce the inflection calculation
if(mode == "I"):
    scaled = np.array(Yerror)*1.2
    parameters, covariance = curve_fit(arcTan, X, Y,sigma=scaled, p0 = guess1799)
    error = np.sqrt(np.diag(covariance))

    grid = np.linspace(energyData.min() - 0.2, energyData.max() + 0.2, 200)
    fitTan = arcTan(grid, *parameters)
    plt.plot(grid, fitTan, '-', label='arctan', color = "black", linewidth = 1)
    plt.axvline(x=abs(parameters[2]), color='red', linestyle='--', label='Resonance')
    plt.scatter(X, Y, label = 'first measurement', c = C, s = 14)
    plt.errorbar(X, Y, yerr=scaled, color = "black", fmt="none", capsize = 3, capthick = 1, elinewidth = 1)
    plt.minorticks_on()
    plt.xlabel("$E_{eff}$ [kV]")
    plt.ylabel("Yield [count/μC]")
    plt.rc('ytick', labelsize=10) 
    plt.rc('xtick', labelsize=10) 
    #plt.xlim(1017.34, 1021.05)
    plt.show()

    print(parameters, error)
    observed_data = np.array(Y)
    expected_data = np.array(arcTan(X, *parameters))
    chi2 = np.sum(((observed_data - expected_data)**2) / (scaled**2))
    print(chi2/len(observed_data))

#reproducibility plot
elif(mode == "R"):
    plt.plot(X2, Y2, '^', markersize = 4, color = "blue", label='second measurement') 
    plt.errorbar(X2, Y2, yerr=Y2error, color = "blue", fmt="none", capsize = 3, capthick = 1, elinewidth = 1)
    plt.legend()

#fit used to produce the width calculation
elif(mode == "W"):
    widthpar, widthcov = curve_fit(targetWidth, X, Y, sigma=Yerror, p0 = guesswidth)
    error = np.sqrt(np.diag(widthcov))

    fitWidth = targetWidth(X, *widthpar)
    plt.plot(X, fitWidth, '-', label='width', color = "black", linewidth = 1)
    plt.arrow(1019.4,55.684,abs(widthpar[2]),0,length_includes_head=True, head_width = 4, head_length=0.3, fc='black', ec='black')
    plt.arrow((1019.4 + (abs(widthpar[2]))), 55.684, -(abs(widthpar[2])), 0, length_includes_head = True, head_width = 4, head_length=0.3, fc='black', ec='black')
    plt.text(1021.1,60, "ΔE = {} keV".format(round(abs(widthpar[2]),2), fontsize=10))
    print(*widthpar)
    print(error)

    plt.show()