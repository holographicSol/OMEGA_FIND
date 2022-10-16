An extremely powerful search and define forensics tool.

""" Written by Benjamin Jack Cullen aka Holographic_Sol

To anyone doing anything they should not be doing, this will get you, and to any journalists crossing the north korean border... i am sorry.

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

    Scan: Scan a directory and try to ascertain if file(s) are what they claim to be.

    Find: A special search feature. Searches for file types not by suffix or MIME types but by reading the file into
    memory and comparing the read to known buffer reads compiled using -learn.

    Define: Return concise/verbose information about a filetype specified.

"""
