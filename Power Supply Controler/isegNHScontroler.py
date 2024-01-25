# -*- coding: utf-8 -*-
"""
Created on Wed Nov  8 14:20:41 2023

@author: Jammie Jones, Personal Email: Jcjones2001@hotmail.co.uk

"""


import time
import pyvisa
import threading
import os
import datetime
import numpy as np 



rm = pyvisa.ResourceManager()

colCh = 0 #colimator channel
targCh = 1 # target channel

################################################
#To configure the click shell layout

from click_shell import shell
import click    

#################################################

#Fetch settings
settings = np.loadtxt('settings.txt',usecols=[1], dtype = 'str')
name, baud, logTime = settings


with rm.open_resource(name) as nhs:
   
    
    nhs.timeout = 4000
    nhs.write_termination = '\n'
    nhs.read_termination = '\n'
    nhs.baudrate = baud
    
    global logStop 
    logStop = True
    
    nhs.write(':VOLT %s,(@%s)' % (0, targCh))
    nhs.read()
    
    nhs.write(':VOLT %s,(@%s)' % (0, colCh))
    nhs.read()
    
    
    @shell(prompt= 'High Voltage >', intro="Voltages being set to zero, type 'help' for a list of commands" )
    def my_app():

        pass

    
    def measureV():
        #col then targ
       
        
        command = (':MEAS:VOLT?(@%s)' %  colCh)
        nhs.query(command)
        time.sleep(.1)
        voltcol = nhs.read().strip()[0:7]
        
        command = (':MEAS:VOLT? (@%s)' %  targCh)
        nhs.query(command)
        time.sleep(.1)
        volttarg = nhs.read().strip()[0:7]
        
      
        
        
       
        
        return (float(voltcol)*1000, float(volttarg)*1000)
    
    def measureA():
        
      
        command = (':MEAS:CURR?(@%s)' %  colCh)
        nhs.query(command)
        time.sleep(.1)
        currcol = nhs.read().strip()[0:7]
        
        command = (':MEAS:CURR? (@%s)' %  targCh)
        nhs.query(command)
        time.sleep(.1)
        currtarg = nhs.read().strip()[0:7]
        
        
        
        
        return currcol, currtarg
    
    
    
        
    
    def readV():
        
       #col then targ
      
       
       command = (':READ:VOLT? (@%s)' %  colCh)
       nhs.query(command)
       voltcol = nhs.read().strip()[0:7]
      
       command = (':READ:VOLT? (@%s)' %  targCh)
       nhs.query(command)
       volttarg = nhs.read().strip()[0:7]
       
       
       return (float(voltcol)*1000, float(volttarg)*1000)



    @my_app.command()
    @click.option('--d',hidden = True,default=888,  type=float)
    def allMeasure(d):
        
        """Displays voltage and current of both channels"""
        if d < 666:
            print(d)
            Dino()
            
        print('ColV:', round(measureV()[0],3) ,'V,', 'ColA:', round(float(measureA()[0]),4) ,'A')
        print('TargV:', round(measureV()[1],3) ,'V,', 'TargA:', round(float(measureA()[1]),4) ,'A')
        
        
    
    @my_app.command()
    def readSetVolts():
        """Displays what voltage channels are set to"""
        print('SET VOLTAGES:')
        volt1, volt2 = readV()
        print('Collimator:   ', volt1)
        print('Target:       ', volt2)
        
    
        
   
        
    @my_app.command()
    @click.argument('volt', required=1)
    def tvolt(volt):#Set target Voltage
        """Sets target voltage, 'tvolt x'"""
        print('TARGET VOLTAGE SET TO %s V' % volt)
      
        nhs.write(':VOLT %s,(@%s)' % (volt, targCh))
        nhs.read()
        
    @my_app.command()
    @click.argument('volt', required=1)
    def cvolt(volt):#Set target Voltage
        """Sets collimator voltage, 'cvolt x'"""
        print('COLLIMATOR VOLTAGE SET TO %s V' % volt)
        nhs.write(':VOLT %s,(@%s)' % (volt, colCh))
        nhs.read()
        
   
            
    
    def log(stopEvent, openEvent, *arg):
        print('Thread started...')
        
            
        ###Incimenting file system!
        
        today = datetime.datetime.today().strftime('%m-%d-%Y')
        i = 0
        while os.path.exists("Logs/Run%s-%s.txt" % (i,today)):
            i += 1
        
        name = "Logs/Run%s-%s.txt" % (i,today)
        print(name)
        f = open(name, "a")
        f.write('Target V, Target C, Colimator V, Collimator C, Time \n')
        
        while True:
            
            time.sleep(int(logTime))
            #print('Logging')
            
            #print(openEvent.is_set(), 's')
            openEvent.wait()
            #print('s in ')
            openEvent.clear()
            
           # print(openEvent.is_set(), 's2')
            #### Write loop code here
            c = datetime.datetime.now()
            
            V = measureV()
            #print(V, 'VV')
            C = measureA()
            t = c.strftime('%H:%M:%S')
            
            f.write('{0},{1},{2},{3},{4} \n'.format(V[1],C[1],V[0],C[0], t))
           # print('{0},{1},{2},{3},{4} \n'.format(V[1],C[1],V[0],C[0], t))
            openEvent.set()
            ####
            #print('s out ')
            if stopEvent.is_set():#Exit event
                
                f.close()
                print('...Thread Ended')
                break
            
        
    
    @my_app.command()
    @click.argument('stepvolt', required=1)
    @click.argument('mintvolt', required=1)
    @click.argument('maxtvolt', required=1)
    @click.argument('gap', required=1)
    def runStep(stepvolt,mintvolt, maxtvolt, gap):
        """
        Performs a full scan of voltages in steps of 'stepvolt',from a min Target voltage 'mintvolt, to a maximum voltage 'maxvolt', with a voltage gap between the two channels of 'gap'.
        While running, a log is produced t
        
        Example: \n
            'runstep 100 300 600 300' - This will run through these values for the target and collimator repectivly: \n
                300V , 0V \n
                400V, 100V \n
                500V, 200V \n
                600V, 300V \n
                END SQUENCE
                
            
        
        """
        stepvolt = int(stepvolt)
        mintvolt = int(mintvolt)
        maxtvolt = int(maxtvolt)
        gap = int(gap)
        
        
        
        ###Start multiprocessing
        openEvent = threading.Event()
        openEvent.set()
        stopEvent = threading.Event()
        stopEvent.clear()
        t1 = threading.Thread(target = log, args = (stopEvent, openEvent,'yes'))
        t1.setDaemon(True)
        t1.start()
        print(t1.ident)
        
        
        
        ##Quick check for numbers to work
        if int(maxtvolt) % int(stepvolt) != 0:
            print('Step amount is not a factor of the maximum voltage')
            return
        
        if int(mintvolt-gap) < 0:
            print('voltage set below 0')
            return
        
        voltage = mintvolt
        for i in range(int((maxtvolt-mintvolt)/stepvolt) + 1):
            
            
            
            #openEvent.wait()
            openEvent.clear() #letting threads know who is accessing what
            time.sleep(.7)
            #print('M in')
            
            #print(openEvent.is_set())
            targVolt = voltage 
            colVolt = voltage - gap
            time.sleep(.1)
            nhs.write(':VOLT {0},(@{1})'.format(targVolt, targCh))
            time.sleep(.1)
            nhs.write(':VOLT {0},(@{1})'.format(colVolt, colCh))
            
            nhs.read()
            nhs.read()
            openEvent.set()
            #print('M out')
            
            print('Target set to {0}V, Collimator set to {1}V...please wait for voltage to ramp'.format(targVolt, colVolt))
            
            #wait for confirmation
            confirm = False
            while confirm == False:
               
               
               openEvent.clear()
               time.sleep(.7)
               x =  measureV()
               openEvent.set()
             
               print(round(x[1], 2), round(x[0], 2))
               if (x[0] > .98*(colVolt- 1) and x[0] < 1.02*(colVolt+1)) and (x[1] > .98*targVolt and x[1] < 1.02*targVolt):
                   confirm = True
                   time.sleep(.2)
            voltage = voltage + stepvolt
            input('Ramped, measure now. Press enter to step...')
            #print('1 min wait...')
            #time.sleep(60)
        print('Sequence complete, setting voltages to 0V')  
        
        
        ###Stop Log
        stopEvent.set()
        time.sleep(1)
        
        nhs.write(':VOLT %s,(@%s)' % (0, targCh))
        nhs.write(':VOLT %s,(@%s)' % (0, colCh))
        nhs.read()
        nhs.read()
        
        time.sleep(1)
        
        def Dino():
            print(r"""  
                  ,
           /|
          / |
         /  /
        |   |
       /    |
       |    \_
       |      \__
       \       __\_______
        \                 \_
        | /                 \
        \/                   \
         |                    |
         \                   \|
         |                    \
         \                     |
         /\    \_               \
        / |      \__ (   )       \
       /  \      / |\\  /       __\____
    snd|  ,     |  /\ \ \__    |       \_
       \_/|\___/   \   \}}}\__|  (@)     )
        \)\)\)      \_\---\   \|       \ \
                      \>\>\>   \   /\__o_o)
                                | /  VVVVV
                                \ \    \
                                 \ \MMMMM                  oh bugger!
                                  \______/         _____ /
                                                  |  O O|
                                                 /___|_|/\_
                                            ==( |          |
                                                 (o)====(o)
    Code Written By Jamie Jones :)                                              
                  """)
    
     
    if __name__ == '__main__':
            my_app()
        

  
    