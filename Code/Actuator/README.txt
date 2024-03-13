WARNING: The servo can do a minimum of 0.01 of a spin, which is 0.00635mm or 0.00025inch. Please keep to factors of these numbers for accuracy


Functions:

-moveXInch n
        This command moves the servo forward x inches, to move backwards format 
        the command 'movexinch -- -x', where x is the amount of inches to move

- moveXmm n
        This command moves the servo forward x mm, to move backwards format 
        the command 'movexmm -- -x', where x is the amount of mm to move

-reset
        Moves the servo back to zero    

-moveToTarget code
        This function will move the servo to a specific point that is obtained from the file 'TargetLocations.txt'.
        The first target is '1', then '2', and so on. More targets can be added, just add a new line and keep the same format
        The units are given in mm from 0.
        
