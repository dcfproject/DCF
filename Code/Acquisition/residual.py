import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np

X = []
Y = np.array([632.23, 991.86, 991.86, 1213.08, 1587.49, 1799.75])
yerror = np.array([0.04, 0.03, 0.03, 0.06, 0.08, 0.09])
# errorbar data
""" with open("C:/Users/Konrad/Desktop/DCF/DCF/Data/Yield/TotalYield_amended.txt", "r") as file:
        for line in file:
            xval, xerr = line.strip().split()
            X.append(float(xval))
            xerror.append(float(xerr))


X = np.array(X)
xerror = np.array(xerror) """

def line(x, m, c):
    val = m*x + c
    return val

X_cross = np.array([649.54373, 1018.95175, 1018.986046, 1246.51863, 1631.19034, 1849.62618])
X = np.array([649.52038207 , 1018.93544145, 1018.90745149, 1246.46296281, 1631.11358864, 1849.55240217])
parameters, covariance = curve_fit(line, X, Y,sigma=yerror, p0 = [0.93,0])
error = np.sqrt(np.diag(covariance))
print(*parameters)
residualsK = Y - line(X, *parameters)
rError = []
for i in range(0, len(X)):
    rError.append(np.sqrt((X[i]*error[0])**2 + error[1]**2 + yerror[i]**2))

print(X, line(X, *parameters))
plt.plot(X, Y, 'o', label='data',markersize = 4)
plt.plot(X, line(X, *parameters), '-', label='fit', linewidth = 1)
plt.text(1200,620, "m = {} ± {} keV/kV".format(round(parameters[0],4), round(error[0],4)), fontsize=12)
plt.text(1200,700, "c = {} ± {} keV".format(round(parameters[1],3), round(error[1],3)), fontsize=12)
plt.xlabel("TV + EV [kV]")
plt.ylabel('Energy [keV]')
plt.minorticks_on()
plt.errorbar(X, Y, yerr=rError, fmt="none")
plt.legend
plt.show()


# Create the residual plot
plt.scatter(X, residualsK, color='r', s=16)  # Create a scatter plot of X vs. residuals
plt.axhline(y=0, color='black', linestyle='--')  # Add a horizontal line at y=0
plt.xlabel('TV + EV [kV]')
plt.ylabel('Residuals [keV]')
plt.minorticks_on()
plt.errorbar(X, residualsK, yerr=yerror, color = "black", fmt="none", capsize = 3, capthick = 1, elinewidth = 1)
plt.show()


fig, (ax0, ax1) = plt.subplots(nrows = 2, sharex = True)


ax0.plot(X, Y, 'o', label='Data',markersize = 5)
ax0.plot(X, line(X, *parameters), '-', label='Fit', linewidth = 1)
#ax0.text(1150,880, "E = m (TV [kV] + EV [kV]) + c [keV]", fontsize=11)
ax0.text(1310,950, r"$\it{E}_{\mathrm{R}}^{\mathrm{lab}} = \it{m} \it{V}_{\mathrm{eff}} + \it{c}$", fontsize=11)
ax0.text(1350,810, " = {} ± {} keV/kV".format(round(parameters[0],4), round(error[0],4)), fontsize=11)
ax0.text(1310,810, "m", fontsize=11, style = "italic")
ax0.text(1350,670, " = {} ± {} keV".format(round(parameters[1],2), round(error[1],2)), fontsize=11)
ax0.text(1310,670, "c", fontsize=11, style = "italic")
ax0.set_ylabel('Energy (keV)', fontsize = 14)
ax0.minorticks_on()
ax0.errorbar(X, Y, yerr=rError, fmt="none")
ax0.set_yticks([600, 1000, 1400, 1800])
ax0.legend(frameon = False, fontsize = 10)

fig.subplots_adjust(hspace = 0.05)

ax1.scatter(X, residualsK, color='r', s=16)  # Create a scatter plot of X vs. residuals
ax1.axhline(y=0, color='black', linestyle='--')  # Add a horizontal line at y=0
ax1.set_xlabel(r"$\it{V}_{\mathrm{eff}}$ (kV)", fontsize = 14)
ax1.set_ylabel('Residuals (keV)', fontsize = 14)
ax1.minorticks_on()
ax1.errorbar(X, residualsK, yerr=rError, color = "black", fmt="none", capsize = 3, capthick = 1, elinewidth = 1)
plt.xticks([600, 1000, 1400, 1800])
#plt.savefig("C:/Users/Konrad/Desktop/residual.png", dpi=1200)
plt.show()
print(rError)