
# Example
The shellcode and the PID of the program you want to inject into needs to be in the programs arguments.

tasklist | findstr /i explorer

.\test.exe shell.b64 48000

