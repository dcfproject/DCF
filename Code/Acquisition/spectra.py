import os
import datetime
import numpy as np
import scipy
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

INITAIL_ROWS = 12

logPath = "C:/Users/Konrad/Desktop/DCF/Data/Logs/27_02_2024"

logFile = open(os.path.join(logPath, "Run_02-27-2024-11_50.txt"), "r")
logStr = logFile.readlines()
logFile.close()
logRaw =  [line.strip().split() for line in logStr[1:] if line.strip()]
logData = np.asarray(logRaw)

spectraPath = "C:/Users/Konrad/Desktop/DCF/Data/Spectra/27_02_2024/Run1"
spectraList = os.listdir(spectraPath)
spectraFile = open(os.path.join(spectraPath, "run0090.Spe"), "r")
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


def gausPol(x, amp, mu, sigma, m, c):
    return m*x + c + amp*(1/(sigma*np.sqrt(2*np.pi)))*np.exp(-1*(x-mu)**2/(2*sigma**2))


def Lorentzian(x, amp1, cen1, wid1):
    return (amp1*wid1**2/((x-cen1)**2+wid1**2))

""" def gausPol(x, amp, mu, sigma, m, c):
    return m*x + c + amp*np.exp(-1*(x-mu)**2/(2*sigma**2)) """

def gaus(x, amp, mu, sigma):
    return amp*np.exp(-1*(x-mu)**2/(2*sigma**2)) 

""" def gausPol(x, amp, mu, sigma):
    return amp*(1/(sigma*np.sqrt(2*np.pi)))*np.exp(-1*(x-mu)**2/(2*sigma**2)) """

def line(x, m, c):
    return m*x + c

xData = np.arange(0, roiRight-roiLeft)
yData = spectraData[roiLeft:roiRight]

pCurve, conCurve = curve_fit(gausPol, xData, yData, p0 = [5000, 50, 20, 0, 20])
perr = np.sqrt(np.diag(conCurve))
pLine, conLine = curve_fit(Lorentzian, xData, yData)

fitCurve = gausPol(xData, pCurve[0], pCurve[1], pCurve[2],pCurve[3],pCurve[4])
fitLine = Lorentzian(xData, pLine[0], pLine[1], pLine[2])


gammaYield = pCurve[0]/(integCharge*10**6)

print(pCurve)
print(gammaYield)



plt.plot(xData, yData, 'o', label='data')
plt.plot(xData, fitCurve, '-', label='Gaussian + 1st polynomial')
plt.legend()
plt.xlabel("Channel")
plt.ylabel("Count")
plt.show()


""" x = np.arange(0, chanelCount)
plt.step(x,spectraData, c= "b")
plt.step(x[roiLeft:roiRight],spectraData[roiLeft:roiRight], c= "r")
plt.yscale("log")
plt.show() """

""" plt.step(x[:roiLeft],spectraData[:roiLeft], c = "b")
plt.step(x[roiLeft:], spectraData[roiLeft:], c = "r") 
plt.yscale("log")
plt.show()
"""