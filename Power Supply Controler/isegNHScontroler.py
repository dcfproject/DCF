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

colCh = "0" #colimator channel
targCh = "1" # target channel

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

    nhs.write(':VOLT ON, (@%s)' % (colCh))
    nhs.read()
    nhs.write(':VOLT ON, (@%s)' % (targCh))
    nhs.read()
    
    nhs.write(':VOLT %s,(@%s)' % (0, targCh))
    nhs.read()

    nhs.write(':VOLT %s,(@%s)' % (0, colCh))
    nhs.read()
    
    
    @shell(prompt= 'High Voltage >', intro="Voltages being set to zero, type 'help' for a list of commands" )
    def my_app():
        pass

    
    def scientific(string):
        return float(string.replace("E", "e")[:-1])

    def measureV():
        #col then targ
       
        command = (':MEAS:VOLT? (@%s)' %  colCh)
        nhs.query(command)
        voltcol = nhs.read().strip()
        
        command = (':MEAS:VOLT? (@%s)' %  targCh)
        nhs.query(command)
        volttarg = nhs.read().strip()

        return scientific(voltcol), scientific(volttarg)
    
    def measureA():
        
        command = (':MEAS:CURR?(@%s)' %  colCh)
        nhs.query(command)
        currcol = nhs.read().strip()
        
        command = (':MEAS:CURR? (@%s)' %  targCh)
        nhs.query(command)
        currtarg = nhs.read().strip()


        return scientific(currcol), scientific(currtarg)
    
        
    def readV():
        
       #col then targ
      
       
       command = (':READ:VOLT? (@%s)' %  colCh)
       nhs.query(command)
       voltcol = nhs.read().strip()
      
       command = (':READ:VOLT? (@%s)' %  targCh)
       nhs.query(command)
       volttarg = nhs.read().strip()

       
       return scientific(voltcol), scientific(volttarg)



    @my_app.command()
    @click.option('--d',hidden = True,default=888,  type=float)
    def allMeasure(d):
        
        """Displays voltage and current of both channels"""
        if d < 666:
            print(d)
            #Dino()
            
        print('ColV:', round(measureV()[0],4) ,'V,', 'ColA:', round(float(measureA()[0]),10) ,'A')
        print('TargV:', round(measureV()[1],4) ,'V,', 'TargA:', round(float(measureA()[1]),10) ,'A')
        
        
    
    @my_app.command()
    def readSetVolts():
        """Displays what voltage channels are set to"""
        print('SET VOLTAGES:')
        volt1, volt2 = readV()
        print('Collimator:   ', volt1, "V")
        print('Target:       ', volt2, "V")
        
    
        
   
        
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
        
    @my_app.command()
    def turnOn():#turn the channels on
        """Turns on the voltage supply channels'"""
        print('ALL CHANNELS ARE ON')
        nhs.write(':VOLT ON, (@%s)' % (colCh))
        nhs.read()
        nhs.write(':VOLT ON, (@%s)' % (targCh))
        nhs.read()




    @my_app.command()
    def turnOff():#turn the channels off
        """Turns off the voltage supply channels'"""
        print('ALL CHANNELS ARE OFF')
        nhs.write(':VOLT OFF, (@%s)' % (colCh))
        nhs.read()
        nhs.write(':VOLT OFF, (@%s)' % (targCh))
        nhs.read()



    def log(stopEvent, openEvent, *arg):
        print('Thread started...')
        
            
        ###Incimenting file system!
        
        today = datetime.datetime.today().strftime('%m-%d-%Y')
        hour = datetime.datetime.now().strftime("%H_%M")
        i = 0
        while os.path.exists("Logs/Run%s-%s.txt" % (today,hour)):
            i += 1
        
        name = "Logs/Run_%s-%s.txt" % (today,hour)
        f = open(name, "a")
        columnName = ["Target_V", "Target_C", "Colimator_V", "Colimator_C", "Time"]
        f.write("{0[0]:<12}{0[1]:<12}{0[2]:<12}{0[3]:<12}{0[4]:<12} \n".format(columnName))
        f.flush()
        
        while True:
            
            time.sleep(int(logTime))

            openEvent.wait()
            #print('s in ')
            openEvent.clear()
            
            #### Write loop code here
            c = datetime.datetime.now()
            
            V = measureV()
            C = measureA()
            t = c.strftime('%H:%M:%S')
            
            f.write('{0:<12}{1:<12}{2:<12}{3:<12}{4:<12} \n'.format(round(V[1],4),round(C[1],4),round(V[0],10),round(C[0],10), t))
            f.flush()
            openEvent.set()
            if stopEvent.is_set():#Exit event
                
                f.close()
                print('...Thread Ended')
                break
            
        
    
    @my_app.command()
    @click.argument('stepvolt', required=1)
    @click.argument('mintvolt', required=1)
    @click.argument('maxtvolt', required=1)
    @click.argument('gap', default = 300)
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
               curr = measureA()

               openEvent.set()
             
               print("Collimator voltage: ",round(x[0], 4), "Target current: ", round(curr[1], 10))
               print("Target voltage: ", round(x[1], 4), "Collimator current: ",round(curr[0], 10))
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
        nhs.read()
        nhs.write(':VOLT %s,(@%s)' % (0, colCh))
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
        

  
    
