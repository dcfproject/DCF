# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             

"""

import serial
import time
import numpy as np
import sys
from click_shell import shell
import click
import cmd



def sendServ(data):
    for byte in data:
        ser.write(byte)
    #print('Sent:', data)
    return
        

def addCRC(data):
    temp = [0]
    i = 0
    
    
    for byte in data:
        i += 1
        temp = [temp[0] + int(byte[0])]
        
          
    crcMask = b'\xFF'
    crcFin = (temp[0] & crcMask[0]).to_bytes(1, byteorder='big')
    
    outPut = data
    outPut.append(crcFin)
   
    return outPut
        

#This is the loop that keeps the port open and closes it when it is finished
port = 'COM3'
with serial.Serial(port) as ser:#CHANGE PORT WHEN NEEDED
    ser.baudrate = 38400 
    ser.port = port
    ser.timeout = 1
    
    @shell(prompt = 'servo >', intro = 
    """
    Starting servo....
    Please enter a command below. If you need a list of all avlible commands type 'help'.
    
    WARNING: The servo can do a minimum of 0.01 of a spin, which is 0.00635mm or 0.00025inch. Please keep to factors of these numbers for accuracy
    """)
    def shell():
       pass
   
    #@shell.command()
   # @click.argument('nspins')
    def movenspins(nspins):
        
        nspins = float(nspins)
        totalSpins = readLoc() + nspins
        
        updateLoc(totalSpins, totalSpins*0.625 )
        ###Checking for negative
        if nspins > 0:
            commandBase = [b'\xFA', b'\x01',b'\xFD',b'\x80',b'\x70',b'\x07'] #Forwards direction
        else:                                                                                       
            commandBase = [b'\xFA', b'\x01',b'\xFD',b'\x10',b'\x70',b'\x07'] #Backwards direction
        nspins = abs(nspins)
        
       
        oneBase =   [ b'\x00',b'\x00',b'\x00',b'\x32']#This represents the amount of puslses, with 00003200 being 1 pulse, 00000032 being .01
        oneBase = b''.join(oneBase)
       
        ### Multiply by 100 to bring into interger amonts of .01 spins
        a = int.from_bytes(oneBase, byteorder = 'big')#Convert to number
        a = a*nspins*64 #multiply by 100 in HEX
        a= int(a)
        
        ###Test for too big
        if a > 4294967100:
            print('Number too big')
            return
        
        a = a.to_bytes(4, byteorder='big')#cahnge back to one single byte

        ###Using loop to make byte readable
        pulseBase = []# This loop seperates the byte to 4 single bytes
        for i in range(4):
            pulseBase.append(a[i].to_bytes(1, byteorder='big'))
       
       
        ###Combine codes
        command = commandBase + pulseBase# join and send the byte
        
        sendServ(addCRC(command))
        
        return
     
        
    @shell.command()
    @click.argument('n')
    def moveXInch(n):
        """ 
        This command moves the servo forward x inches, to move backwards format 
        the command 'movexinch -- -x', where x is the amount of inches to move
        """
        n = float(n)
        #.01 turns = 0.00625mm
        #.01 turns = 0.00025 inch
        #1 inch = 40 turns
        
        amountOfTurns = n*40
        movenspins(amountOfTurns)
        
        
    @shell.command()
    @click.argument('n')
    def moveXmm(n):
        
        """ 
        This command moves the servo forward x mm, to move backwards format 
        the command 'movexmm -- -x', where x is the amount of mm to move
        """
       # n = float(n)
        
        #.01 turns = 0.00625mm
        #.01 turns = 0.00025 inch
        #1 inch = 40 turns
        
        amountOfTurns = float(n)*1.6
       # print('gsfdgsg')
        movenspins(amountOfTurns)
        
        
        
    def updateLoc(x,y):
        #Rewrites the current locations
        np.savetxt('currentLoc.txt', [[x],[y]])
        return
     
        
     
    def readLoc():
        #reads the current location
        x = np.loadtxt('currentLoc.txt')[0]
        return float(x)
     
        
    
    def spinToZero():

        movenspins(-4.3*40)
        time.sleep(50)
        
        #stp the moter to not waste time after an amount of seconds
        command = [b'\xFA', b'\x01',b'\xF6',b'\x00',b'\x00',b'\x00',b'\x00',b'\x00',b'\x00',b'\x00']
        sendServ(addCRC(command))
        ser.read(8)#Read started stopping
        time.sleep(2)
        ser.read(8)#read fail or success
        time.sleep(2)
        
        
        movenspins(2)#Moving 2 steps forward to aline to zero
        ser.read(8)
        
        print('...Set to Zero')
        
        
        
    @shell.command()    
    def reset():
        """
        Moves the servo back to zero
        """
        
        print('Initiating reset, moving to position zero..')
        print('Please wait 60 seconds...')
        spinToZero()
        updateLoc(0,0)
        print('...Done')
        
        
    @shell.command()
    @click.argument('code')
    def moveToTarget(code):
        """
        This function will move the servo to a specific point that is obtained from the file 'TargetLocations.txt'.
        The first target is '1', then '2', and so on. More targets can be added, just add a new line and keep the same format
        The units are given in mm from 0.
        """
        
        code = int(code)
        #get target locations
        print('Moving to target', code)
        x = np.loadtxt('targetLocations.txt', skiprows = 0, usecols = [1], dtype = 'str', delimiter = ',')
   
        targetPlaceMm = float(x[code-1]) #target distance in spins
        inspinsFromZero = targetPlaceMm*1.6 #Convert to mm
        differenceFromCurrentLoc = inspinsFromZero - readLoc() #take difference
        
        movenspins(differenceFromCurrentLoc) #move difference
        return
        
    
    
    
    

    
    if __name__ == '__main__':
        shell()
            


    
    #print(readLoc())
   # moveXmm(0)
    #moveToTarget(2)
    
    


    
    
    
    
    
    
    
  
       
