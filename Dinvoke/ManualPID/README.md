
# Example
The PID of the program you want to inject into needs to be the first argument. However the shellcode can be placed in the program. I have found the detection rate varies on what shellcode is in the program.

tasklist | findstr /i explorer

.\test.exe 48000

