def arg(configfile, arg):
	f = open(configfile)

	for line in f:
	    line = line.strip()
	    
	    if arg in line:
	        if line[0] == "#":
	        	value = ""

	        else:
	        	value = line.split('=')[1]


	f.close()
	return value