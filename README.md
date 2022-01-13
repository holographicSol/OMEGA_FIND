deobfuscate ~ Written by Benjamin Jack Cullen aka Holographic_Sol

Step 1: Read file(s) into the buffer to try and check its true file type.
Step 2. Scan for the file(s) suffix in the database.
Step 3. Compare the database definition of the files suffix to the results from step 1.

Designed to distinguish between obfuscated files and non-obfuscated files.

An in this case definition of what is meant by obfuscated file: A file that has had its file name suffix modified in attempt to
disguise the file as another file type.
Example: File foobar.mp4 has been renamed to anything.exe

This program can be used as is to scan for obfuscated files, define file types and machine learn. Can also be used creatively to create technologies that use this programs ability to distinguish between known files and obfuscated files as part of some
other function. For example Apple does this to prevent performing certain actions with some file types regardless of
the files alleged suffix.
