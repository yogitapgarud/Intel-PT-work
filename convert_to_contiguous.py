
def convert_to_multik(file1, file2):
	prev, start_address = '0', None
	count = 0

        with open(file1,'r') as fr, open(file2, 'w+') as fw:
		for line in fr:
                        line = line.split()
                        address = line[0]
                        address = hex(int(address, 16))

			if 'L' in address:
				address = address[:-1]

			if not start_address:
				start_address = address
				count = 1
			
			if 'L' in prev:
				prev = prev[:-1]

			#print(prev, address, hex(int(prev, 16)+1))
			addone = hex(int(prev, 16)+1)
			#print(prev, address, addone)

			if 'L' in addone:
				addone = addone[:-1]

	                #print(prev, address, addone)

			if addone == address:
				count += 1

			elif prev != '0':
				count = hex(count)[2:]
				fw.write(start_address+","+count+"\n")
				start_address = address
				count = 1

			prev = address

		count = hex(count)[2:]
        	fw.write(start_address+","+count+"\n")

convert_to_multik("/home/b/workspace_Yogita/ls_expand_addess11.out", "/home/b/workspace_Yogita/ls_11_multik.out")
