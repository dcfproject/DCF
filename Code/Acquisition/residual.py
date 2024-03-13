import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np
from sklearn.linear_model import LinearRegression

X = []
xerror = []
""" Y = np.array([632.2, 991.8, 991.8, 1213.1, 1587.5, 1799.7])
yerror = np.array([3.34e-3, 35e-3, 35e-3, 50e-3, 100e-3, 100e-3]) """
Y = np.array([991.8, 991.8, 1213.1, 1587.5])
yerror = np.array([35e-3, 35e-3, 50e-3, 100e-3])
# errorbar data
with open("C:/Users/Konrad/Desktop/DCF/Data/Yield/TotalYield_amended.txt", "r") as file:
        for line in file:
            xval, xerr = line.strip().split()
            X.append(float(xval))
            xerror.append(float(xerr))

""" X = np.array([649.50717, 1018.93329, 1018.87931, 1246.42354, 1630.89411, 1849.58757])
Y = np.array([632.2, 991.8, 991.8, 1213.1, 1587.5, 1799.7]) """

# errorbar data amended
""" X = np.array([649.50717, 1018.93329, 1018.87931, 1246.42354, 1631.06272, 1849.58757])
Y = np.array([632.2, 991.8, 991.8, 1213.1, 1587.5, 1799.7]) """

def line(x, m, c):
    val = m*x + c
    return val

X = np.array(X)
xerror = np.array(xerror)
parameters, covariance = curve_fit(line, X, Y, sigma=yerror, p0 = [0,0])
error = np.sqrt(np.diag(covariance))

residualsK = Y - line(X, *parameters)

print(X, line(X, *parameters))
plt.plot(X, Y, 'o', label='data')
plt.plot(X, line(X, *parameters), '-', label='fit')
plt.text(1300,1200, "m = {} ± {} keV/kV".format(round(parameters[0],5), round(error[0],5)), fontsize=10)
plt.text(1300,1100, "c = {} ± {} keV".format(round(parameters[1],5), round(error[1],5)), fontsize=10)
plt.title('Energy vs accelerator parameters')
plt.xlabel('TV + EV - Bias (kV)')
plt.ylabel('Energy(keV)')
plt.errorbar(X, Y, xerr = xerror, yerr=yerror, fmt="none")
plt.show()


# Create the residual plot
plt.scatter(X, residualsK)
plt.axhline(y=0, color='r', linestyle='--')  # Add a horizontal line at y=0
plt.xlabel('TV + EV - Bias (kV)')
plt.ylabel('Residuals (keV)')
plt.title('Residual Plot')
plt.errorbar(X, residualsK, yerr=yerror, fmt="none")
plt.show()




# Fit a linear regression model

""" # Create an instance of the LinearRegression model
model = LinearRegression()

# Reshape the X array to a 2D array
X = X.reshape(-1, 1)

# Fit the model to the data
model.fit(X, Y)

# Get the slope and intercept of the fitted line
slope = model.coef_[0]
intercept = model.intercept_

# Print the slope and intercept
print("Slope:", slope)
print("Intercept:", intercept)

# Plot the data and the fitted line
plt.plot(X, Y, 'o', label='data')
plt.plot(X, model.predict(X), '-', label='fit')
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Linear Regression')
plt.legend()
plt.show() """