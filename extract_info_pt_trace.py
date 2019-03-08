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

    for key, value in sym_count.iteritems():
        x.add_row([key, value])

    print(x)
    print("Total symbols = ", len(sym_count))

path = os.getcwd()
filename = "mapped_addresses_ls3.out"
dirname = "new-ls-traces-4.4.11/"
file_pt_trace = os.path.join(path, dirname+filename)
#print(file_pt_trace)

count_syscalls(file_pt_trace)
