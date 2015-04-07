#!/bin/bash

host='pi'
port='5432'

sendcmd () {
	echo "PIN=$1,OUT,$2" | busybox nc $host $port
}

getstate () {
	state=$(echo "PIN=$1,IN,0" | busybox nc $host $port)
	echo $state
}

if [ "$2" == '-' ]; then
	pinstate=$(getstate $1)
	if [ "$pinstate" == '0' ]; then
		sendcmd $1 1
	elif [ "$pinstate" == '1' ]; then
		sendcmd $1 0
	fi
else
	sendcmd $1 $2
fi
