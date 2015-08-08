import json, os, sys, time, datetime, traceback


pathname = os.path.dirname(sys.argv[0])        
fullpath = os.path.abspath(pathname)

config_file = fullpath + "/config/config.json"
data_file = fullpath + "/data.json"

delay = 20



def success(x):

    hostname = data_object['People'][x]['hostname']
    name = data_object['People'][x]['name']
    online = True

    current_time = str(datetime.datetime.now()).rsplit(".")[0].rsplit(":",1)[0]

    data_object['People'][x] = {
        
        "hostname": hostname,
        "name": name,
        "online": online,
        "last_seen": current_time

    }

def fail(x):

    hostname = data_object['People'][x]['hostname']
    name = data_object['People'][x]['name']
    online = False

    last_seen = ''

    try:
        last_seen = data_object['People'][x]['last_seen']
    except Exception:
        print '\n'
        traceback.print_exc()
        print '\n'

    if last_seen == '':
        data_object['People'][x] = {
        
            "hostname": hostname,
            "name": name,
            "online": online

        }
    else:
        data_object['People'][x] = {
        
            "hostname": hostname,
            "name": name,
            "online": online,
            "last_seen": last_seen

        }


def pinghost(people, x):
    
    # global pingthreads

    
        
    ip = os.system("ping -c 1 " + people[x]['hostname'] + " >> /dev/null")      
    print "PING - pinging %s returned %s" % (people[x]['hostname'], ip)
               
    if ip == 0:
        # msg = str("PERSON ," + person['name'] + ",IN")
        # self.sendMessage(msg)

        success(x)

    else:
        # msg = str("PERSON ," + person['name'] + ",OUT")
        # self.sendMessage(msg)

        fail(x)
            
    
def update_people_list():
    ### Get people
    with open(config_file) as conf_file:
        json_data = json.load(conf_file)
        people = json_data['Web']['People']

    return people


############################

people = update_people_list()


### reset data file
## get file contents
with open(data_file) as d_file:
    data_object = json.load(d_file)
    

## overwrite people array and write updated contents to file
with open(data_file, 'w') as d_file:
    data_object['People'] = []
    data_object['People'] = people

    d_file.write(json.dumps(data_object, indent=4))

### setup done!

def main():
    global people

    while 1:
        ### start pinging
        
        for x in range(0, len(people)):
            print "PING - Trying to ping %s..." % people[x]['hostname']
            pinghost(people, x)
        
        
        ### write results to file
        
        data_to_file = json.dumps(data_object, indent=4)
        
        
        with open(data_file, 'w') as d_file_out:
            d_file_out.write(data_to_file)

        print "PING - Sleeping for %s seconds..." % delay
        time.sleep(delay)

        print "PING - Updating people list..."
        people = update_people_list()


