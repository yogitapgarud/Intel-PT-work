import os
from prettytable import PrettyTable

def get_strace(program, filename):
    os.system("strace -o " + program)

def count_syscalls(filename, file_pt_trace):
    syscall_count = {}
    syscalls_set = set()

    x = PrettyTable()
    x.field_names = ["Symbol", "Strace Count", "Intel PT Count"]

    with open(filename, 'r') as fr:
        lines = fr.readlines()
        lines = lines[:-1]

        for line in lines:
            func = line.split('(')[0]
            syscall_count[func] = syscall_count.get(func, 0) + 1
            syscalls_set.add(func)
            #print(func)

    #print(syscall_count)

    #for key in syscall_count.iteritems():
    symbol_count = {}

    with open(file_pt_trace, 'r') as fr:
        for line in fr:
            #print(line)
            sym = line.split()
            if len(sym) > 1:
                sym = sym[1]
                for s in syscalls_set:
                    cmp = "sys_"+s
                    #print(s,sym)
                    if cmp == sym:
                        #print(s)
                        symbol_count[sym] = symbol_count.get(sym, 0) + 1
                        #print(sym, symbol_count[sym])

    for key, value in syscall_count.iteritems():
        print(key)
        x.add_row([key, value, symbol_count["sys_"+key]])

    print(x)
    #print(symbol_count)

def syscall_sequence_check(file_strace, file_pt_trace):
    syscall_sequence = []
    mapping = {'execve' : 'return_from_execve',
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
                'unlink' : 'sys_unlink'
              }

    with open(file_strace, 'r') as fr:
        lines = fr.readlines()
        lines = lines[:-1]

        for line in lines:
            func = line.split('(')[0]
            syscall_sequence.append(func)

        syscall_sequence = syscall_sequence[:115] + syscall_sequence[117:]

    i = 0
    n = len(syscall_sequence)

    with open(file_pt_trace, 'r') as fr:
        for line in fr:
            sym = line.split()[1]
            if mapping[syscall_sequence[i]] == sym:
                print(syscall_sequence[i], sym)
                i += 1
                if i == n:
                    break

    print("Count matched in sequence: ", i, len(syscall_sequence), syscall_sequence[i:])


prog_ls = "ls"
path = os.getcwd()
dir_name = "new-ls-traces-4.4.11/"
filename_strace = "strace_ls.txt"

dir_name = "gzip-traces-March5/"
filename_strace = dir_name+"strace_gzip.txt"
file_pt_trace = os.path.join(path, dir_name+"mapped_addresses_gzip3.out")

#get_strace(prog_ls)

#count_syscalls(filename_strace, file_pt_trace)
syscall_sequence_check(filename_strace, file_pt_trace)
