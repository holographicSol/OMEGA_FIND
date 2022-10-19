An extremely powerful search and define forensics tool. Written by Benjamin Jack Cullen aka Holographic_Sol.

OMEGA FIND

Intention 1: To find/expose files that may be pretending to be a file type other than the files real file type.

    Example: secret_file.mp4 has been renamed to anything.anything and buried somewhere in a drive.
        OMEGA FIND seeks to expose these files for what they really are.
        (A double-edged blade. agent exposes you/you expose an agent)

Intention 2: To find files not by name or filename suffix matching but by reading each file into memory and comparing
    the buffer to known buffer reads for the suffix specified.

Intention 3: Define. Specify a filename suffix and return a concise/verbose description of the file type specified.

Modes of operation:

    Learn: Provide OMEGA FIND with a directory path of trusted file(s) to learn from to build OMEGA FINDS knowledge of
    what file types should look like.

    De-Obfuscate: Scan a directory and try to ascertain if file(s) are what they claim to be.

    Scan: A special search feature. Searches for file types not by suffix or MIME types but by reading the file into
    memory and comparing the read to known buffer reads compiled using -learn.

    Define: Return concise/verbose information about a filetype specified.

Command line arguments:

--de-obfuscate    Specifies a directory to scan.
-learn            Instructs the program to learn from a specified location. Only use trusted locations/files.
-scan             Specify path. Finds files predicated upon known buffer read associations created by learning.
                  A special and powerful search feature.
-define           Attempts to lookup a definition for suffix specified.'

--buffer-size     Specify in bytes how much of each file will be read into the buffer.
                  If using --buffer-size full, then a scan/learning/find operation could take a much longer time.
                  --buffer-size can be used in combination with -scan, -learn and -find.
-suffix           Specify suffix. Used in combination with -find.
-v                Output verbose. Only recommended when using -define and for development purposes.
-h                Displays this help message

Example: omega_find --buffer-size 2048 -scan C:\ -suffix mp4
Example: omega_find --buffer-size 2048 -learn C:\
Example: omega_find --buffer-size full --de-obfuscate C:\
Example: omega_find -v -define jpg

OmegaFind is only as good as its implementation. A working knowledge of filesystems is recommended in order to best
implement OmegaFind.