# Importing libraries that will be used
import numpy as np
import datetime
import os
import matplotlib.pyplot as plt
import scipy
from scipy.optimize import curve_fit

# Get the list of all files and directories
INITAIL_ROWS = 12
runEnergy = "1799"

logPath = "C:/Users/Konrad/Desktop/DCF/Data/Logs/"
logList = os.listdir(os.path.join(logPath, runEnergy))

spectraPath = "C:/Users/Konrad/Desktop/DCF/Data/Spectra/"
spectraList = os.listdir(os.path.join(spectraPath, runEnergy))

csvFile= open("C:/Users/Konrad/Desktop/DCF/Data/DCF1799.csv")
csvClean = [c.strip().split() for c in csvFile if c.strip()]

energy = []
totalYield = []
errorYield = []

def gausPol(x, amp, mu, sigma, m, c):
    return amp*(1/(sigma*np.sqrt(2*np.pi)))*np.exp(-1*(x-mu)**2/(2*sigma**2)) + m*x + c

count = 0
for log in logList:
    allspectra = os.listdir(os.path.join(spectraPath, runEnergy , spectraList[count]))
    logFile = open(os.path.join(logPath, runEnergy, log), "r")
    logStr = logFile.readlines()
    logFile.close()
    logRaw =  [line.strip().split() for line in logStr[1:] if line.strip()]
    logData = np.array(logRaw)

    for spec in allspectra:
        spectraFile = open(os.path.join(os.path.join(spectraPath, runEnergy , spectraList[count]), spec), "r")
        spectraStr = spectraFile.readlines()
        spectraFile.close()

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
        current = np.asanyarray(logData[int(index1):int(index2)+1,1], dtype=float)
        currentDiff = max(abs(np.diff(current, n = 4)))
        integCharge = scipy.integrate.cumulative_simpson(y = current)[-1]
        integError = currentDiff*timeChange**5 /(180*len(current)**4)

        roiLeft, roiRight  = spectraStr[2062].strip().split(" ")
        roiLeft = int(roiLeft) 
        roiRight = int(roiRight)

        chanelCount = int(spectraStr[11].strip().split(" ")[1])
        spectraData = np.zeros(chanelCount)
        for i in range(0,chanelCount):
            spectraData[i] = int(spectraStr[i+INITAIL_ROWS])

        for i in csvClean:
            run = str(i).split(",")
            if(run[1] + ".Spe" == spec):
                energy.append(float(run[10]))
                break
            elif(run[3] + ".Spe" == spec):
                energy.append(float(run[12]))
                break

        print(energy[-1],spec)

        xData = np.arange(0, roiRight-roiLeft)
        yData = spectraData[roiLeft:roiRight]

        ppar, pcov = curve_fit(gausPol, xData, yData, p0 = [5000, 60, 20, 0, 20])
        perr = np.sqrt(np.diag(pcov))

        fitCurve = gausPol(xData, *ppar)
        gammaYield = ppar[0]/(integCharge*10**6)
        plt.plot(xData, yData, 'o', label='data')
        plt.plot(xData, fitCurve, '-', label='Gaussian + 1st polynomial')
        plt.legend()
        plt.xlabel("Channel")
        plt.ylabel("Count")
        plt.show()
        totalYield.append(abs(gammaYield))
        errorYield.append(abs(gammaYield)*np.sqrt((perr[0]/ppar[0])**2 + (integError/(integCharge*10**6))**2))
    count += 1
f = open("C:/Users/Konrad/Desktop/DCF/Data/Yield/YieldData_1799_2.txt", "w")
for l in range(0,len(totalYield)):
    f.write(str(energy[l]) + " " + str(totalYield[l]) + " " + str(errorYield[l]) + "\n")
f.close    
    




