deobfuscate ~ Written by Benjamin Jack Cullen aka Holographic_Sol

---------------------------------------------------------------------------------------------------------------------------------------
Designed to distinguish between obfuscated files and non-obfuscated files.

    An in this case definition of what is meant by obfuscated file: A file that has had its file name suffix modified in attempt to
    disguise the file as another file type.
    Example: File foobar.mp4 has been renamed to anything.exe

---------------------------------------------------------------------------------------------------------------------------------------
De-Obfuscate (whatis) ~ Written by Benjamin Jack Cullen aka Holographic_Sol

    Designed to distinguish between obfuscated files and non-obfuscated files.
    In this particular definition of what is meant by obfuscated file: A file that has had its file name suffix modified in
    attempt to disguise the file as another file type.
    Example: File foobar.mp4 has been renamed to anything.exe
    This program also attempts to define a given extension for you.
    This program can also learn from user specified locations in order to potentially perform more accurate deobfuscation.
---------------------------------------------------------------------------------------------------------------------------------------

Command line arguments:

    -s                Specifies a directory to scan. [whatis -s directory_name -v]
    -d                Attempts to lookup a definition for suffix (not file/directory name) given. [whatis -d exe -v]
    --machine-learn   Instructs the program to train from a specified location. [whatis --machine-learn directory_name -v]
    -v                Show verbose output
    -h                Displays this help message

---------------------------------------------------------------------------------------------------------------------------------------
Scan:

    Scan a specified location for obfuscated files.
    Step 1: The file(s) read in buffer to try and check its true file type.
    Step 2: Scans for the file(s) alleged suffix in the database.
    Step 3: A digitless database definition is then compared to a digitless result from Step 1.
    Results are logged and also displayed during the scan and upon scan completion.

---------------------------------------------------------------------------------------------------------------------------------------
Machine Learn:

    Learns from a specified location.
    Step 1: The file(s) read in buffer to try and check its file type.
    Step 2: New buffer/suffix associations are (learned) appended to the machine learning database.
    Results are logged and also displayed during machine learning and upon machine learning completion.
    Care should be taken that no obfuscated files are in the specified location.

---------------------------------------------------------------------------------------------------------------------------------------
Summary:
    This program can be used as is to scan for obfuscated files, define file types and machine learn. Can also be used
    creatively in harmony with technologies that need to distinguish between known files and obfuscated files as part of
    some other function. For example Apple does this to prevent performing certain actions with some file types regardless
    of the files alleged suffix.
