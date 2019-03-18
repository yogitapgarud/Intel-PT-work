import os
from prettytable import PrettyTable

def classify_extra_symbols(filename):
    sym_count = {}
    x = PrettyTable()
    x.field_names = ["Symbol", "Count"]

    with open(filename, 'r') as fd:
        for line in fd:
            sym = line.split()[0]
            sym_count[sym] = sym_count.get(sym, 0) + 1
    
    #print(sym_count)

    total_syms = 0
    classes = {"perf": 0, "selinux": 0, "page": 0, "lock": 0, "sched": 0,
               "ext4": 0, "rcu": 0, "cache": 0, "write": 0, "map":0,
               "pt_":0, "tty":0, "security":0, "time": 0, "inode": 0, "task":0,
               "process":0, "irq":0 }

    for key, value in sym_count.iteritems():
        for k, v in classes.iteritems():
            #print(k)
            if k in key:
                classes[k] += value
                total_syms += value

    y = PrettyTable()
    y.field_names = ["Symbol"]

    for k, v in classes.iteritems():
        x.add_row([k, v])

    print(x)

    for key, value in sym_count.iteritems():
        y.add_row([key])

    print(y)

    print(total_syms)

path = os.getcwd()
filename = "not_in_strace_ls3.txt"
#dirname = "new-ls-traces-4.4.11/"

file_pt_trace = os.path.join(path, filename)
#print(file_pt_trace)

classify_extra_symbols(file_pt_trace)