SCT_FILE_PARSER

*******************************
Version 2.0.1
Created on 5/6/2020
Last update: 5/13/2020 1300 MT
Created By Nikolas Boling
Special thanks to Kyle Sanders
For Entertainment Purposes Only, Not for real world use!
*******************************

This program is intended for Vatsim VRC Sector files for each ARTCC. 
It will go through the sector file for the ARTCC and create individual txt files
for each section of the sector file. Once its complete you can change out a 
specific section (text file) with what you need. Then you can recompile it back
into one .sct2 file. This program will create the files inside a folder located
where the program EXE is located called "Sector_Files". 

Side note Kyle Sanders has created a .BAT file that will combine all txt files 
back into one sector file. The .bat file can be found on GitHub with the following link.
https://github.com/KSanders7070/Combine_TXT_Into_SCT - Again All Credit for 
this batch file and the idea of my program goes to Kyle Sanders.


Please post any issues you come across on GitHub under the Issues tab and I will
try to correct them as they come in. 

*******************************
Requirements:
	Sector File must be located where the program EXE file is located.
	Sector File Must be named "SECTOR.SCT2"
	EXE must be located where it does not need ADMIN permissions to create files.
	Does not have a folder called "Sector_Files" inside of the directory the exe is.
*******************************
Feature Requests: 
	Simple GUI
	Option to Combine back into one Sector File

*******************************
Known Issues:
	Crash on startup if the above requirements are not met.
	Must have a sector file to decompile.

*******************************
Change Log: 
	Version 1.2.0:
		Added version checker. Everytime the program starts up it will check 
		github to see if the current versions match. If they do nothing will
		happen and the program will continue. However, if they do not match
		it will notify the user of the new release on github. Maybe in the future
		it will ask if you want to download the newest version.

	Version 1.1.2:
		Changed output to Console to be a little bit more clear with what it is
		doing. For Example, the console will now tell you when it is making the
		different header files i.e. [AIRPORTS], [COLORS], [INFO].
		
		Added Pause at the end to make sure the user knows it completed correctly
		and withought errors. 
	
	Version 1.1.1:
		"Missing Data" will now be appended before "true File name" to really stand 
		out in the folder. Example "__MISSING_DATA__10212_ENV_ENV .txt"

	Version 1.1.0:
		Fixes program crash if the sector file has an IAP that does not have
		any data assigned to it. For example "ENV_ENV " is one that did not have
		any data inside, so the program crashed when it reached this point.
		
		The program will now still create the text file but in the naming will
		will have "__MISSING_DATA__" appended to the end of the file name and 
		will no longer crash.
		
		This may change in the future to either Exclude the IAP and notify 
		the user or list it in a different folder. Update for this soon to come.
*******************************