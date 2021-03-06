# GCM File Organizer

Simple Python software to help you organize your files

Usage:

-m [origin] [destination]
  
Moves files under the [origin] directory (and its subdirectories) to the directories listed in [destination], according to the files' extension. The expected formats for [origin] and [destination] are:

[origin]:
    
    /home/myuser/mydir/

[destination]:
    
    pdf,doc,docx:/home/myuser/documents/?mp3:/home/myuser/musics/?cpp,java,py,php:/home/myuser/code/
        
Note that ",", ":", and "?" act as separator. An usage example using the examples above is:
        
    python gcm_file_organizer -m /home/myuser/mydir/ pdf,doc,docx:/home/myuser/documents/?mp3,ogg:/home/myuser/musics/?cpp,java,py,php:/home/myuser/code/
    
**WARNING!** Files with same name in [origin] and/or [destination] will be overrided in the [destination] by the last copy found. That's something to be fixed in the future.
    

-c [reference] [dirs_to_check] [options]
    
Checks [dirs_to_check] (and its subdirectories) for duplicates of the files in [reference] (and its subdirectories). The result is saved to a file (default, because the output can be very extensive) or printed in the terminal, if the "--ocli" is used. [reference] and [dirs_to_check] have the following formats:
    
[reference]: 

    /home/myuser/mydir/

[dirs_to_check]:
    
    /home/myuser/documents/?/home/myuser/code/
        
It also has some options:
    
--ocli -> Prints the output to the current terminal.
    
--pnr -> Outputs the names of the unique files in <reference>, instead of the duplicated ones.
        
Example:

    python gcm_file_organizer -c /home/myuser/mydir/ /home/myuser/documents/?/home/myuser/code/
