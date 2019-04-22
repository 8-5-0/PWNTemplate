#! /usr/bin/env python

import argparse
import re
import os,stat

if __name__ == "__main__":
    template_raw = """
#! /usr/bin/env python2
# Author: 850
from pwn import *
import os
\"\"\"
pwn script framework
\"\"\"

class BASE(object):
    def __init__(self, remote_host, remote_port, local_elf, gdb_script, _remote_libc, _local_libc, _log_level):
        \"\"\"
        initial basic paramaters
        \"\"\"
        self.rhost = remote_host
        self.rport = remote_port
        self.elf_name = local_elf
        self.gdb_scripts = gdb_script
        self.local_libc = _local_libc
        self.remote_libc = _remote_libc
        context(os='linux', log_level=_log_level)
        context(terminal=["xfce4-terminal", "-e"])

    def local_debug(self, gdb_attach):
        \"\"\"
        debug with GDB
        \"\"\"
        self.target = process(self.elf_name)
        self.elf = ELF(self.elf_name)
        self.libc = ELF(self.local_libc)
        if gdb_attach:
            gdb.attach(self.target, gdbscript=self.gdb_scripts)

    def remote_attack(self,):
        \"\"\"
        remote exploit
        \"\"\"
        self.libc = ELF(self.remote_libc)
        self.target = remote(self.rhost, self.rport)
        self.elf = ELF(self.elf_name)
    
    def run(self,):
        # self.local_debug(gdb_attach=True)
        # self.remote_attack()
        return "done"

solve = BASE(
    remote_host="{RemoteHost}",
    remote_port={RemotePort},
    local_elf="./{LocalELF}",
    _remote_libc="{RemoteLibc}",
    _local_libc="{LocalLibc}",
    gdb_script="",
    _log_level="info"
)
print solve.run()
"""

    parser = argparse.ArgumentParser()
    parser.add_argument("-b", "--bin", help="binaryfile", type=str)
    parser.add_argument("-u", "--url", help="remote url", type=str)
    parser.add_argument("-p", "--port", help="remote port", type=str)
    parser.add_argument("-l", "--llibc", help="local libc", type=str)
    parser.add_argument("-r", "--rlibc", help="remote libc", type=str)
    args = parser.parse_args()

    (rh, rp, binary, rlibc, llibc) = (args.url,
                                      args.port, args.bin, args.rlibc, args.llibc)

    generated = template_raw.format(RemoteHost=rh, RemotePort=rp,
                              LocalELF=binary, RemoteLibc=rlibc, LocalLibc=llibc)
    outfile = open("./what_pwn.py", "w")
    outfile.write(generated)
    outfile.close()
    os.chmod("./what_pwn.py", 0o755)