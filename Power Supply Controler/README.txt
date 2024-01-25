Hey! 

This is a command line interface based program, type 'help' to get the list of commands avalible
To find out what each command does, and what arguments are needed, type the command followed by '--help' or '-h'

Functions:

-allmeasure
	 Displays voltage and current of both channels

-readSetVolts
	Displays what voltage channels are set to

-tvolt x
	Sets target voltage to 'x'

-cvolt x
	Sets collimator voltage to 'x'

-runstep stepvolt maxvolt gap
	
        Performs a full scan of voltages in steps of 'stepvolt',from a min Target voltage 'mintvolt, to a maximum voltage 'maxvolt', 
	with a voltage gap between the two channels of 'gap'.
        While running, a log is produced t
        
        Example: \n
            'runstep 100 300 600 300' - This will run through these values for the target and collimator repectivly: \n
                300V , 0V \n
                400V, 100V \n
                500V, 200V \n
                600V, 300V \n
                END SQUENCE
                
            
        