#!/bin/bash

# SCRIPT PARALLEL LOCKING
LOCKFILE=/tmp/get_ifconfig.sh.lock

if [[ -f $LOCKFILE ]]; then
	echo "CT_FAILED: Script already running!"
	exit 1
fi

touch $LOCKFILE
trap 'rm -rf $LOCKFILE' EXIT


# ERROR HANDLING
set -e

catch() {
	if [ "$1" != "0" ]; then
		echo "CT_FAILED: Execution error!"
		# DO SOMETHING ON ERROR
	fi
}

trap catch ERR SIGINT SIGTERM SIGHUP SIGQUIT


# SCRIPT

ifconfig
