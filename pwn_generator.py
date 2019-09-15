#! /usr/bin/env python3

import argparse
import re
import os
import magic

if __name__ == "__main__":
    template_raw = """#! /usr/bin/env python2
# Author: 850
from pwn import *
import os,re
\"\"\"
pwn script framework
\"\"\"

class BASE(object):
    def __init__(self, 
                _remote_host, 
                _remote_port, 
                _local_elf, 
                _break_points_addr, 
                _break_points_symbol, 
                _remote_libc, 
                _local_libc, 
                _log_level
                ):
        \"\"\"
        initial basic paramaters
        \"\"\"
        self.offset = 0
        self.rhost = _remote_host
        self.rport = _remote_port
        self.elf_name = _local_elf
        self.bps = (_break_points_addr, _break_points_symbol)
        self.local_libc = _local_libc
        self.remote_libc = _remote_libc
        context(os='linux', log_level=_log_level)
        context(terminal=["lxterminal", "-e"])

    def local_debug(self, gdb_attach):
        \"\"\"
        debug with GDB
        \"\"\"
        self.target = process(self.elf_name)
        print(hex(self.offset))
        self.elf = ELF(self.elf_name)
        self.libc = ELF(self.local_libc)
        if self.elf.pie:
            _vmmap = open("/proc/{{}}/maps".format(self.target.pid), "r").read()
            _regex = "^.*r-xp.*{{}}.*$".format(os.path.abspath(self.elf_name))
            _line = [_ for _ in _vmmap.split("\\n") if re.match(_regex, _)][0]
            self.offset = int(_line.split("-")[0], 16)
        if gdb_attach:
            _gdb_script = "\\n".join(['b *{{}}'.format(hex(self.offset+_)) for _ in self.bps[0]])
            _gdb_script += "\\n".join(['b {{}}'.format(_) for _ in self.bps[1]])
            gdb.attach(self.target, gdbscript=_gdb_script)

    def remote_attack(self,):
        \"\"\"
        remote exploit
        \"\"\"
        self.libc = ELF(self.remote_libc)
        self.target = remote(self.rhost, self.rport)
        self.elf = ELF(self.elf_name)
    
    def run(self,):
        # self.local_debug(gdb_attach=False)
        # self.local_debug(gdb_attach=True)
        # self.remote_attack()
        return "done"

solve = BASE(
    _remote_host="{RemoteHost}",
    _remote_port={RemotePort},
    _local_elf="{LocalELF}",
    _remote_libc="{RemoteLibc}",
    _local_libc="{LocalLibc}",
    _break_points_addr=[],
    _break_points_symbol=[],
    _log_level="info",
)
print(solve.run())
"""

    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--directory", help="directory", type=str)
    parser.add_argument("-r", "--remote", help="remote url", type=str)
    args = parser.parse_args()

    remote_libc = "/lib/x86_64-linux-gnu/libc-2.27.so"
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
        raise Exception("No excutable binary found")
    if remote_libc == "/lib/x86_64-linux-gnu/libc-2.27.so":
        print("[*]No remote libc found, use local libc by default.")
    remote_host = args.remote
    if not ":" in remote_host:
        raise Exception("Invalid remote host or port.")
    generated = template_raw.format(
        RemoteHost=remote_host[:remote_host.find(':')],
        RemotePort=remote_host[remote_host.find(':')+1:],
        LocalELF=binary, 
        RemoteLibc=remote_libc, 
        LocalLibc="/lib/x86_64-linux-gnu/libc-2.27.so",
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
