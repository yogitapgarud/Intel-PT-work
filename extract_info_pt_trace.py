import os
from prettytable import PrettyTable

def count_syscalls(file_pt_trace):
    sym_count = {}
    syscalls_set = set()
    x = PrettyTable()

    x.field_names = ["Symbol", "Count"]

    with open(file_pt_trace, 'r') as fr:
        for line in fr:
            sym = line.split()[1]
            sym_count[sym] = sym_count.get(sym, 0) + 1

    total_syms = 0
    classes = {"perf": 0, "selinux": 0, "page": 0, "lock": 0, "sched": 0,
               "ext4": 0, "rcu": 0, "cache": 0, "write": 0}

    for key, value in sym_count.iteritems():
        x.add_row([key, value])
        total_syms += value

        for k, v in classes.iteritems():
            #print(k)
            if k in key:
                classes[k] += value

    print(x)
    print("Unique symbols = ", len(sym_count))
    print("Total  symbols = ", total_syms)
    print(classes)

path = os.getcwd()
filename = "mapped_addresses_ls_sw_1.out"
dirname = "new-ls-traces-4.4.11/"

#dirname = "gzip-traces-March5/"
#filename = "mapped_addresses_gzip1.out"

#dirname = "pwd-March7/"
#filename = "mapped_addresses_pwd1.out"

file_pt_trace = os.path.join(path, dirname+filename)
#print(file_pt_trace)

count_syscalls(file_pt_trace)
