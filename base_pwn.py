#! /usr/bin/env python2
# Author: 850
from pwn import *
import os
"""
pwn script framework
"""

class BASE(object):
    def __init__(self, remote_host, remote_port, local_elf, gdb_script, _remote_libc, _local_libc, _log_level):
        """
        initial basic paramaters
        """
        self.rhost = remote_host
        self.rport = remote_port
        self.elf_name = local_elf
        self.gdb_scripts = gdb_script
        self.local_libc = _local_libc
        self.remote_libc = _remote_libc
        context(os='linux', log_level=_log_level)
        context(terminal=["xfce4-terminal", "-e"])

    def local_debug(self, gdb_attach):
        """
        debug with GDB
        """
        self.target = process(self.elf_name)
        self.elf = ELF(self.elf_name)
        self.libc = ELF(self.local_libc)
        if gdb_attach:
            gdb.attach(self.target, gdbscript=self.gdb_scripts)

    def remote_attack(self,):
        """
        remote exploit
        """
        self.libc = ELF(self.remote_libc)
        self.target = remote(self.rhost, self.rport)
        self.elf = ELF(self.elf_name)
    
    def run(self,):
        return "done"

solve = BASE(
    remote_host="",
    remote_port=8080,
    local_elf="",
    _remote_libc="./libc.so.6",
    _local_libc="/lib64/libc.so.6",
    gdb_script="",
    _log_level="info"
)
print solve.run()
