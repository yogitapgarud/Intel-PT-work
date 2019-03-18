import os

def read_file(file1, file2):
	with open(file1,'r') as fr, open(file2, 'w+') as fw:

	    	for line in fr:
			if '[' in line:
				continue
			else:
				line = line.split()
				address, length = line[1], line[2]
				address = hex(int(address, 16))[2:]
				address = address if 'L' not in address else address[:-1]
				#print(address, length)
				fw.write(address+','+length+'\n')

def merge_read(file1, file2):
	prev = None

        with open(file1,'r') as fr, open(file2, 'w+') as fw:

                for line in fr:
                        if '[' in line:
                                continue
                        else:
                                line = line.split()
                                address, length = line[1], line[2]
				hex_add = hex(int(address, 16)) + int(length)
                                offset = hex(int(address, 16)-0xffffffff81000000)[2:-1]
                                fw.write(offset+'\n')
				prev_length = length

def expand_intelpt(file1, file2):
	with open(file1,'r') as fr, open(file2, 'w+') as fw:
		for line in fr:
			line = line.split(',')
			address, count = line[0], line[1]
			address = hex(int(address, 16))
			if 'L' in address:
				address = address[:-1]
			count = int(count)

			for i in range(count):
				#print(address)
				fw.write(address[2:]+"\n")
				address = hex(int(address, 16)+1)
				if 'L' in address:
					address = address[:-1]


def expand_qemu(file1, file2):
        with open(file1,'r') as fr, open(file2, 'w+') as fw:
                for line in fr:
                        line = line.split(',')
                        address, count = line[0], line[1]
                        address = hex(int(address, 16))
			if "\n" in count:
				count = count[:-1]
			count = "0x"+count
			#print(count)
                        count = int(count,  0)
			#fw.write(address+","+count)

                        for i in range(count):
                                fw.write(address[2:]+"\n")
                                address = hex(int(address, 16)+1)

def offset_to_address(file1, file2):
	with open(file1,'r') as fr, open(file2, 'w+') as fw:
	#with open(file1,'r') as fr:
		for line in fr:
			line = line.split()
			offset = line[0]
			address = hex(int(offset, 16)+0xffffffff81000000)[2:]
			#print(address)
			address = address if 'L' not in address else address[:-1]
			#print(offset, address)
			address = address
			#print(address)
			#os.system("cat ./kallsyms | grep " + address)
			fw.write(address+"\n")

def map_address_kallsyms(file1):
	with open(file1,'r') as fr:
		for line in fr:
			line = line.split()
			offset = line[0]
			address = hex(int(offset, 16))[2:]
			#print(address)
			address = address if 'L' not in address else address[:-1]
			#print(offset, address)
			address = address
			#print(address)
			os.system("cat ./kallsyms | grep " + address)
			#fw.write(address+"\n")

def get_symbol_kallsyms(kallsyms, file_expand_address, mapped_addresses):
	symbol_mapping = {}
	with open(kallsyms, 'r') as fr:
		for line in fr:
			line = line.split()
			if len(line) > 1:
				symbol_mapping[line[0]] = line[2]
				#print(line[0], line[2])

	with open(file_expand_address, 'r') as fe, open(mapped_addresses, 'w+') as fw:
		for line in fe:
			line = line.split()
			#print(line[0])
			if line[0] in symbol_mapping:
				#print(line[0])
				fw.write(line[0]+" "+symbol_mapping[line[0]]+"\n")

path = os.getcwd()
#print(path)
#dir_name = "gzip-traces-March5/"
#filename = "gzip_pt3.out"

dir_name = "ls-varied-buffer/"
filename = "ls_ulimit16384.out"

filepath_original = os.path.join(path, dir_name+filename)
#print(filepath_original)

suffix_name = os.path.splitext(filename)[0]
file_offset = os.path.join(path, dir_name+suffix_name+"_offset.out")
file_address = os.path.join(path, dir_name+suffix_name+"_address.out")
file_expand_length = os.path.join(path, dir_name+suffix_name+"_expand_offset.out")
file_expand_address = os.path.join(path, dir_name+suffix_name+"_expand_address.out")
#file_mapped_kallsyms = os.path.join(path, dir_name+suffix_name)

read_file(filepath_original, file_address)
expand_intelpt(file_address, file_expand_address)

#expand_qemu("/home/yogita/Downloads/ls.trace", "/home/yogita/processor-trace/ls_expand_qemu.out")

#offset_to_address(file_expand_length, file_expand_address)

#map_address_kallsyms(file_expand_address)

mapped_addresses = os.path.join(path, dir_name+"mapped_addresses_ls_ulimit16384.out")
get_symbol_kallsyms("./kallsyms", file_expand_address, mapped_addresses)
