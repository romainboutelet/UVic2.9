**INITIAL SETUP--THE INSTRUCTIONS MAY NEED UPDATES (last update 23/06/2021)** 

This directory contains the base code that runs the EnKF on top of the UVic Climate Model. This directory should be named "pynetcdf" and placed in the MOBI2.0 directory. 
The main code files are listed as "exe_file.py" and "exe2fwf_file.py". These are two different forms of the EnKF : "exe_file.py" uses only 1 freshwater input location (North Atlantic) and "exe2fwf_file.py" uses both freshwater inputs in the North Atlantic and in the Southern Ocean.

To be functional, the EnKF code needs the following :

- a directory located on /MOBI2.0/ containing the ensemble subdirectories named as following : "ensname$" with $ being from 0 to n-1. Each of these subdirectory must be set up as a copy of the same version of the UVic model with the same parameters. The "restart.nc" file must also be the same in all of the subdirectories. When copying the subdirectories, don't forget to update the "******.q" file with the right path for each subdirectory.
Concerning updates (implementing the right "fwa.h" "gosbc.F" "setmom.F" and "UVic_ESCM.F" versions) : 

- a subdirectory that contains the observations used in the EnKF. The current set up is to have a tavg file produced previously. The tavg file must have been produced such that the "runlen", "timavgint", "timavgper" are the same than in the "exe_file.py" file. That means the tavg file must have the same averaging periods than what is used in the EnKF code.
