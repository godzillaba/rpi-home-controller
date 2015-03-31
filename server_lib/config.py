import logging
def arg(configfile, arg):
	try:
            f = open(configfile)
	except IOError as e:
            logging.critical("Config file not found: %s", e)
            exit()
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
