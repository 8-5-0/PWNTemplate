#! /usr/bin/env python3
# Author: 850
from pwn import *
import os,re,argparse
"""
pwn script framework
"""

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
        """
        initial basic paramaters
        """
        self.offset = 0
        self.rhost = _remote_host
        self.rport = _remote_port
        self.elf_name = _local_elf
        self.bps = (_break_points_addr, _break_points_symbol)
        self.local_libc = _local_libc
        self.remote_libc = _remote_libc
        context(os='linux', log_level=_log_level)
        context(terminal=["xfce4-terminal", "-e"])

    def local_debug(self, gdb_attach):
        """
        debug with GDB
        """
        self.target = process(self.elf_name)
        print(hex(self.offset))
        self.elf = ELF(self.elf_name)
        self.libc = ELF(self.local_libc)
        if self.elf.pie:
            _vmmap = open("/proc/{{}}/maps".format(self.target.pid), "r").read()
            _regex = "^.*r-xp.*{{}}.*$".format(os.path.abspath(self.elf_name))
            _line = [_ for _ in _vmmap.split("\n") if re.match(_regex, _)][0]
            self.offset = int(_line.split("-")[0], 16)
        if gdb_attach:
            _gdb_script = "\n".join(['b *{{}}'.format(hex(self.offset+_)) for _ in self.bps[0]])
            _gdb_script += "\n" + "\n".join(['b {{}}'.format(_) for _ in self.bps[1]])
            gdb.attach(self.target, gdbscript=_gdb_script)

    def remote_attack(self,):
        """
        remote exploit
        """
        self.libc = ELF(self.remote_libc)
        self.target = remote(self.rhost, self.rport)
        self.elf = ELF(self.elf_name)
    
    def run(self,gdb_attach):
        # self.local_debug(gdb_attach=gdb_attach)
        # self.remote_attack()
        return "done"

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Standard Pwn script')
    parser.add_argument('--debug',action="store_true")
    parser.add_argument('--gdb',action="store_true")
    args = parser.parse_args()
    
    log_level = "debug" if args.debug else "info"
    
    solve = BASE(
        _remote_host="{RemoteHost}",
        _remote_port={RemotePort},
        _local_elf="./{LocalELF}",
        _remote_libc="{RemoteLibc}",
        _local_libc="{LocalLibc}",
        _break_points_addr=[],
        _break_points_symbol=[],
        _log_level=log_level,
    )
    print(solve.run(args.gdb))
