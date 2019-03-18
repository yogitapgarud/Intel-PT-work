import os

def merge_pt_traces(dir_name, subcalls_file):
    merged_symbols = set()

    for filename in os.listdir(dir_name):
        print(filename)
        path = os.getcwd()

        with open(os.path.join(path, dir_name+"/"+filename), 'r') as f1:
            for line in f1:
                sym = line.split()[1]
                merged_symbols.add(sym)
                #print(sym)

    print("Total symbols: ", len(merged_symbols))

    strace_symbols = set()

    with open(subcalls_file, 'r') as fs:
        for line in fs:
            line = line.split()
            strace_symbols.add(line[0])
            #print(line[0])

    print("Symbols in strace: ", len(strace_symbols))
    print("Symbols common in merged and strace: ", len(set.intersection(strace_symbols, merged_symbols)))

merge_pt_traces("ls-all", "subcalls_ls_size512.txt")