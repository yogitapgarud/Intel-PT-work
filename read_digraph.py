import os
from collections import deque
import json

calling = {}
functions = {}
id_mapping = {}
func_to_file_mapping = {}
files_id = {}

def read_digraph():
    '''
    calling = {}
    functions = {}
    id_mapping = {}
    '''
    count = 0

    with open('diagraph_defconfig.txt', 'r') as f:
        for line in f:
            edge = line.split("\"")

            if len(edge) > 1:
                node1 = edge[1]
                if "." in node1:
                    index = node1.index(".")
                    node1 = node1[:index]
                if node1 not in functions:
                    functions[node1] = count
                    id_mapping[count] = node1
                    count += 1
                    #print(node1)

            if len(edge) > 3:
                node2 = edge[3]
                if "." in node2:
                    index = node2.index(".")
                    node2 = node2[:index]
                if node2 not in functions:
                    functions[node2] = count
                    id_mapping[count] = node2
                    count += 1

                id1 = functions[node1]
                id2 = functions[node2]

                if id1 in calling:
                    calling[id1].add(id2)

                else:
                    calling[id1] = set()
                    calling[id1].add(id2)

            #if "->" in edge[2]:
            #    node2 = edge[3]
        

            #print(line)
            #print(node1)
        #print("total functions: ", len(functions))
        #print(calling)

def get_all(s):

    queue = deque(list(s))
    #print(queue)
    visited = set()

    while queue:
        node = queue.popleft()
        visited.add(node)

        if node in calling:
            currd = calling[node]

        for n in currd:
            if n not in visited:
                queue.append(n)
                s.add(n)

    return s

def get_dependencies(function_name):

    func_id = functions[function_name]
    print("id : ", func_id)

    if func_id in calling:
        direct = calling[func_id]
        all_d = get_all(direct)

    else:
        print("no dependencies")

    d = set()

    for i in all_d:
        d.add(id_mapping[i])
    
    #print(d)
    return d

def process_file(file_name):
	file_count = -1

	with open(file_name, 'r') as ins:
		for line in ins:
			split_line = line.split(" ")

			if len(split_line) == 4:
				if split_line[0] == ";;" and split_line[1] == "Function" and split_line[3][0] == '(' and split_line[3][-1] == ')':
					func_name = split_line[2]
		            
				func_id = functions[func_name]

				if file_name not in files_id:
					file_count += 1
					files_id[file_name] = file_count

			func_to_file_mapping[func_id] = file_count

def function_to_files():

	count = 0

	for root, dirs, files in os.walk("."):
		for file in files:
			if file.endswith(".expand"):
				file_name = os.path.join(root, file)
				#print(os.path.join(root, file))
				process_file(file_name)
				count += 1
	print("total files: ", count)

def get_functions():
    files_functions = {}
    set_files = set()

    with open('nginx_test_function_trace.txt', 'r') as file:
        for line in file:
            split_line = line.split()
            #print("splitted line: ", split_line)
            calling_func = split_line[4]
            sinc = split_line[5]
            sinc = sinc[2:]
            print("functions:", calling_func, sinc)
            
            set_files.add(func_to_file_mapping[calling_func])
	    #files_functions[calling_func] = fileforfunc1
            set_files.add(func_to_file_mapping[sinc])
            #files_functions[sinc] = fileforfunc2
            
    with open('all_files_to_include.txt', 'w') as wfile:
        for s in set_files:
            wfile.write(s)
            wfile.write("\n")

if __name__ == "__main__":
    
    read_digraph()

    while True:
        print("Do you want to find dependencies? 1. Yes 2. No")
        ans = int(input())

        if ans == 1:
            print("which function?")
            func = input()
            d = get_dependencies(func)

            for i in d:
                print(i)
            print("Total dependencies: ", len(d))
            #print(d)

        else:
            break
