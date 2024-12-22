import os
import datetime
import numpy as np
import scipy
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

INITAIL_ROWS = 12

logPath = "C:/Users/Konrad/Desktop/DCF/Data/Logs/1799"

logFile = open(os.path.join(logPath, "Run_02-28-2024-17_56.txt"), "r")
logStr = logFile.readlines()
logFile.close()
logRaw =  [line.strip().split() for line in logStr[1:] if line.strip()]
logData = np.asarray(logRaw)

spectraPath = "C:/Users/Konrad/Desktop/DCF/Data/Spectra/1799/Run2"
spectraList = os.listdir(spectraPath)
spectraFile = open(os.path.join(spectraPath, "run0252.Spe"), "r")
spectraStr = spectraFile.readlines()
spectraFile.close()


#pull time information from the spectra to correlate it with the log file
startTime = datetime.datetime.strptime(spectraStr[7].strip(), '%m/%d/%Y %H:%M:%S')
timeChange = int(spectraStr[9].strip().split(" ")[0])
newTime = datetime.timedelta(seconds = timeChange) 
stopTime = startTime + newTime 

index1 = np.where( logData == str(startTime)[11:])[0]
while (len(index1) == 0):
    startTime = startTime - datetime.timedelta(seconds = 1) 
    index1 = np.where( logData == str(startTime)[11:])[0]

index2 = np.where( logData == str(stopTime)[11:])[0]
while (len(index2) == 0):
    stopTime = stopTime - datetime.timedelta(seconds = 1) 
    index2 = np.where( logData == str(stopTime)[11:])[0]


#Charge integral using Cumulatively composite Simpson’s 1/3 rule
current = np.asanyarray(logData[int(index1):int(index2)+1,1], dtype=float)
currentDiff = max(abs(np.diff(current, n = 4)))
integCharge = scipy.integrate.cumulative_simpson(y = current)[-1]
integError = currentDiff*timeChange**5 /(180*len(current)**4)

x = np.arange(0, len(current))
plt.plot(x, current*10**6)
plt.xlabel("Time (s)")
plt.ylabel("Current (μA)")
plt.show()
print(integCharge, integError)

print(integCharge, integError)

roiLeft, roiRight  = spectraStr[2062].strip().split(" ")
roiLeft = int(roiLeft) 
roiRight = int(roiRight)


chanelCount = int(spectraStr[11].strip().split(" ")[1])
spectraData = np.zeros(chanelCount)
for i in range(0,chanelCount):
    spectraData[i] = int(spectraStr[i+INITAIL_ROWS])


def gausPol(x, area, mu, sigma, m, c):
    return area*(1/(sigma*(np.sqrt(2*np.pi))))*np.exp(-1*(x-mu)**2/(2*sigma**2)) + m*x + c


c = 23.656767 
m = 2.297974
x = np.arange(c, m*chanelCount+c, m)
xData = np.arange(m*roiLeft+c,m*roiRight+c,m)
yData = spectraData[roiLeft:roiRight]

plt.step(x[:roiLeft],spectraData[:roiLeft], c = "black")
plt.step(xData,yData, c= "r")
plt.step(x[roiRight:], spectraData[roiRight:], c = "black") 
plt.yscale("log")

plt.show()


