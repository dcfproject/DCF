import numpy as np
import matplotlib.pyplot as plt

df = np.loadtxt("C:/Users/Konrad/Desktop/DCF/DCF/Data/Yield/Yield_binned/Yield_992_full.txt")
energy = df[:,0]
yieldData = df[:,1]
yerror = df[:,2]

stab = np.loadtxt("C:/Users/Konrad/Desktop/DCF/DCF/Data/Yield/YieldData_Stability.txt")
stabEnergy = stab[:,0]
stabData = stab[:,1]
yerrorStab = stab[:,2]
xData = np.arange(2,2*(len(stabData)+1),2)

model = np.loadtxt("C:/Users/Konrad/Desktop/DCF/DCF/Data/Yield/Model/992.txt")
x = model[:,0]
y = model[:,1]




stab = [1019.08, 1018.60, 1019.0, 1018.60]
print(stab[2]-stab[3])

# Plot the residuals
plt.plot(energy, yieldData, "o", color = "blue", markersize = 3, label = "Resonance scan")
plt.errorbar(energy, yieldData, yerr=yerror, color = "blue", fmt="none", capsize = 3, capthick = 1, elinewidth = 1)
plt.plot(stabEnergy, stabData, "o", markersize = 3, label = "Stability data", color = "g")
plt.plot(x, y, color = "blue", label = "Fit")
plt.axvline(x = stab[2], c = "r", linestyle='--')
plt.axvline(x = stab[3], c = "r", linestyle='--')



#plt.axvline(x=0, color='r', linestyle='--')  # Add horizontal line at y=0
plt.xlabel('TV + EV - Bias (kV)', fontsize = 14)
plt.ylabel('Yield (a.u.)', fontsize = 14)
plt.legend(frameon = False)
plt.show()


fig, (ax0, ax1) = plt.subplots(ncols = 2, sharey = True)

# Plot the stability scan
ax0.plot(xData, stabData, 'o', label='Stability data', color = "green", markersize = 5)
ax0.errorbar(xData, stabData, yerr=yerrorStab, color = "green", fmt="none", capsize = 3, capthick = 1, elinewidth = 1)
ax0.set_xlabel("Time (min)", fontsize = 14)
ax0.set_ylabel("Yield (a.u.)", fontsize = 14)
ax0.legend(frameon = False, loc = "upper left", fontsize = 10)
ax0.tick_params(axis='both', which='major', labelsize=12)

fig.subplots_adjust(wspace = 0.05)

# Plot the voltage drift scan
ax1.plot(stabEnergy, stabData, "o", markersize = 5, label = "Stability data", color = "g")
ax1.plot(energy, yieldData, "o", color = "blue", markersize = 5, label = "Resonance scan")
ax1.errorbar(energy, yieldData, yerr=yerror, color = "blue", fmt="none", capsize = 3, capthick = 1, elinewidth = 1)
ax1.plot(x, y, color = "blue", label = "Fit")
ax1.axvline(x = stab[0], c = "r", linestyle='--')
ax1.axvline(x = stab[1], c = "r", linestyle='--')

#plt.axvline(x=0, color='r', linestyle='--')  # Add horizontal line at y=0
ax1.set_xlabel('TV + EV - Bias (kV)', fontsize = 14)
ax1.legend(frameon = False, loc = "lower right", fontsize = 10)
ax1.tick_params(axis='both', which='major', labelsize=12)
plt.gcf().set_size_inches(8, 4)
plt.tight_layout()
#plt.savefig("C:/Users/Konrad/Desktop/stab.pdf", dpi=1200)
plt.show()