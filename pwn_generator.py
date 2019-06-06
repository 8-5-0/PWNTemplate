#! /usr/bin/env python

import argparse
import re
import os
import stat

if __name__ == "__main__":
    template_raw = """#! /usr/bin/env python2
# Author: 850
from pwn import *
import os,re
\"\"\"
pwn script framework
\"\"\"

class BASE(object):
    def __init__(self, _remote_host, _remote_port, _local_elf, _break_points, _remote_libc, _local_libc, _log_level):
        \"\"\"
        initial basic paramaters
        \"\"\"
        self.offset = 0
        self.rhost = _remote_host
        self.rport = _remote_port
        self.elf_name = _local_elf
        self.bps = _break_points
        self.local_libc = _local_libc
        self.remote_libc = _remote_libc
        context(os='linux', log_level=_log_level)
        context(terminal=["xfce4-terminal", "-e"])

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
            _gdb_script = "\\n".join(['b *{{}}'.format(hex(self.offset+_)) for _ in self.bps])
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
    _local_elf="./{LocalELF}",
    _remote_libc="{RemoteLibc}",
    _local_libc="{LocalLibc}",
    _break_points=[],
    _log_level="info",
)
print(solve.run())
"""

    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--directory", help="directory", type=str)
    parser.add_argument("-r", "--url", help="remote url", type=str)
    parser.add_argument("-p", "--port", help="remote port", type=str)
    args = parser.parse_args()

    remote_libc = "/lib64/libc.so"
    current_files = os.listdir(args.directory)
    for i in current_files:
        if ".so" in i:
            remote_libc = i
        else:
            binary = i

    generated = template_raw.format(
        RemoteHost=args.url,
        RemotePort=args.port,
        LocalELF=binary, 
        RemoteLibc=remote_libc, 
        LocalLibc="/lib64/libc.so.6",
        )
    outfile = open("./pwn_" + binary + ".py", "w")
    outfile.write(generated)
    outfile.close()
    os.chmod("./pwn_" + binary + ".py", 0o755)
