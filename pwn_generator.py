#! /usr/bin/env python3

import argparse
import re
import os,sys
import magic

if __name__ == "__main__":
    with open(os.path.dirname(os.readlink(sys.argv[0]))+"/template.py", 'r') as f:
        template_raw = f.read()

    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--directory", help="directory where ", type=str)
    parser.add_argument("-r", "--remote", help="remote url", nargs=2, type=str)
    args = parser.parse_args()

    remote_libc = "/lib/x86_64-linux-gnu/libc.so.6"
    try:
        current_files = os.listdir(args.directory)
        abs_dir = os.path.abspath(args.directory)
    except:
        raise Exception("No such directory")
    binary = ''
    
    for i in current_files:
        try:
            if not os.path.isdir(abs_dir+"/"+i):
                if "ELF" in magic.from_file(abs_dir+"/"+i):
                    if ".so" in i:
                        remote_libc = i
                    elif ".dbg" in i:
                        # support dwg's bundle
                        binary = i
                    else:
                        binary = i
        except:
            pass
    if binary == '':
        print("No excutable binary found, Generate anyway?[Y/N]")
        choice = input()
        if choice != 'Y' and choice != 'y':
            raise Exception("No excutable binary found")
        binary = "anything"
    if remote_libc == "/lib/x86_64-linux-gnu/libc.so.6":
        print("[*]No remote libc found, use local libc by default.")
    remote_host = args.remote
    # print(remote_host)
    try:
        _ = int(remote_host[1])
        isIP = re.compile('^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')
        if not isIP.match(remote_host[0]):
            raise Exception("Invalid remote host or port.")
    except:
        raise Exception("Invalid remote host or port.")
    generated = template_raw.format(
        RemoteHost=remote_host[0],
        RemotePort=int(remote_host[1]),
        LocalELF=binary, 
        RemoteLibc=remote_libc, 
        LocalLibc="/lib/x86_64-linux-gnu/libc.so.6",
        )
    script_file = abs_dir + "/pwn_" + binary + ".py"
    if os.path.exists(script_file):
        raise Exception("EXP Script has already been created")
    print("[*]Writing to file:\n" + script_file)
    outfile = open(script_file, "w")
    outfile.write(generated)
    outfile.close()
    print("[*]Grant X permission")
    os.chmod(abs_dir + "/pwn_" + binary + ".py", 0o755)
    print("[*]EXP script generated, happy pwning.")
