import os
import re
from collections import deque
from prettytable import PrettyTable

db_called = {}

def count_symbols_in_diagraph(diagraph, mapped_ksyms):
    funcs = set()

    with open(diagraph, 'r') as fd:
        for line in fd:
            line = line.split()
            #print(line)

            if len(line) > 2:
                start, end = line[0].strip('"'), line[2].strip('"')
                #print(start, end)
                funcs.add(start)
                funcs.add(end)

            else:
                #print(line[0].strip('"'))
                s = line[0].strip('"')
                funcs.add(s)
    
    with open(mapped_ksyms, 'r') as fsyms:
        counted = set()

        for line in fsyms:
            sym = line.split()[1]
            if sym in funcs:
                counted.add(sym)

    print("Symbols in diagraph: ", len(counted))

def save_graph(diagraph):

    with open(diagraph, 'r') as fd:
        for line in fd:
            line = line.split()
            #print(line)

            if len(line) > 2:
                start, end = line[0].strip('"'), line[2].strip('"')
                #print(start, end)
                start, end = start.lower(), end.lower()
                #if start == "sys_rt_sigaction":
                #    print(start, end)

                if start in db_called:
                    db_called[start].append(end)

                else:
                    db_called[start] = []
                    db_called[start].append(end)

            else:
                #print(line[0].strip('"'))
                s = line[0].strip('"')
                if s not in db_called:
                    db_called[s] = []

def search_graph(symbol):

    queue = deque()
    if symbol in db_called:
        queue.append(symbol)
        #print("in search graph", symbol)
    else:
        return

    all_descend = set()

    while queue:
        curr = queue.popleft()
        all_descend.add(curr)

        if curr in db_called:
            #print("add: ", curr, db_called[curr])
            for item in db_called[curr]:
                if item not in all_descend:
                    queue.append(item)

    return all_descend

def find_subcalls(strace_file, subcalls_found):
    mapping = {'execve' : 'execve',
                'brk' : 'sys_brk',
                'access' : 'sys_access',
                'open' : 'sys_open',
                'fstat' : 'sys_newfstat',
                'mmap' : 'sys_mmap',
                'close' : 'sys_close',
                'read' : 'sys_read',
                'mprotect' : 'sys_mprotect',
                'arch_prctl' : 'sys_arch_prctl',
                'munmap' : 'sys_munmap',
                'set_tid_address' : 'sys_set_tid_address',
                'set_robust_list' : 'sys_set_robust_list',
                'rt_sigaction' : 'sys_rt_sigaction',
                'rt_sigprocmask' : 'sys_rt_sigprocmask',
                'getrlimit' : 'sys_getrlimit',
                'statfs' : 'sys_statfs',
                'ioctl' : 'sys_ioctl',
                'getdents' : 'sys_getdents',
                'write' : 'sys_write',
                'exit_group' : 'sys_exit_group',
                'rt_sigaction' : 'sys_rt_sigaction',
                'rt_sigprocmask' : 'sys_rt_sigprocmask',
                'utimensat' : 'sys_utimensat',
                'fchown' : 'sys_fchown',
                'fchmod' : 'sys_fchmod',
                'rt_sigprocmask' : 'sys_rt_sigprocmask',
                'lseek' : 'sys_lseek',
                'unlink' : 'sys_unlink',
                'getcwd' : 'sys_getcwd'
              }

    syscall_count = {}
    syscalls_set = set()

    x = PrettyTable()
    x.field_names = ["Symbol", "Strace Count", "Intel PT Count"]

    strace_list = set()

    with open(strace_file, 'r') as fr:
        lines = fr.readlines()
        lines = lines[:-1]

        for line in lines:
            func = line.split('(')[0]
            strace_list.add(mapping[func])


    with open(subcalls_found, 'w+') as fw:

        for syscall in strace_list:
            subs = search_graph(syscall)
            #print(syscall)
            #print(subs)
            if subs:
                for s in subs:
                    fw.write(s+"\n")

def compare_subcalls_to_mapped_symbols(subcalls_file, mapped_ksyms):
    s1, s2 = set(), set()

    with open(subcalls_file, 'r') as fs:
        for line in fs:
            line = line.split()
            s1.add(line[0])
            #print(line[0])

    with open(mapped_ksyms, 'r') as fr:
        for line in fr:
            line = line.split()[1]
            s2.add(line)

        common = set.intersection(s1, s2)

        with open("common_ls_ulimit16384.txt", 'w+') as fw:
            for c in common:
                fw.write(c+"\n")

    inMappedSymsOnly = s2 - s1

    with open("not_in_strace_ls_ulimit16384.txt", 'w+') as fn:
        for item in inMappedSymsOnly:
            fn.write(item+"\n")

    inStraceOnly = s1 - s2

    with open("not_in_strace_ls_ulimit16384.txt", 'w+') as fn:
        for item in inMappedSymsOnly:
            fn.write(item+"\n")

    with open("not_in_mapped_syms_ls_ulimit16384.txt", 'w+') as fm:
        for item in inStraceOnly:
            fm.write(item+"\n")

    print("Common in both:          ", len(common))
    print("Only occuring in strace: ", len(inStraceOnly))
    print("Total symbols in strace: ", len(s1))

def compare_functions_not_present():
    s1, s2 = set(), set()

    with open("not_in_mapped_syms_ls_size512.txt", 'r') as fm:
        for line in fm:
            line = line.split()[0]
            s1.add(line)

    with open("not_in_mapped_syms_ls_size4096.txt", 'r') as fs:
        for line in fs:
            line = line.split()[0]
            s2.add(line)

    print("not common: ", len(s1-s2), len(s2-s1))

path = os.getcwd()
diagraph_file = "diagraph_defconfig-441.txt"
dir_name = "ls-varied-buffer/"
strace_file = os.path.join(path, dir_name+"strace_new_ls.txt")
mapped_ksyms = os.path.join(path, dir_name+"mapped_addresses_ls_ulimit16384.out")

"""
count_symbols_in_diagraph(diagraph_file, mapped_ksyms)

save_graph(diagraph_file)

find_subcalls(strace_file, "subcalls_ls_ulimit16384.txt")
"""
compare_subcalls_to_mapped_symbols("subcalls_ls_ulimit16384.txt", mapped_ksyms)


#compare_functions_not_present()