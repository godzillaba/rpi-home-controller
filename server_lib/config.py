def arg(configfile, arg):
	f = open(configfile)
	value = ""
	for line in f:
	    line = line.strip()
	    
	    if arg in line:
	        if line[0] == "#":
	        	value = ""

	        elif "=" in line:
	        	value = line.split('=')[1]
	        else:
	        	value = line


	f.close()
	return value