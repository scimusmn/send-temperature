#!/bin/sh

# Use the smc command line tool to read the TA0P sensor
# This sensor is the Ambient Air temperature
# Data is in Celsius
# Use sed and perl to parse the value into only the digits
temp="$(smc -k TA0P -r | sed 's/.*bytes \(.*\))/\1/' | sed 's/\([0-9a-fA-F]*\)/0x\1/g' | perl -ne 'chomp; ($low,$high) = split(/ /); print(((hex($low)*256)+hex($high))/4/64);')"

echo Ambient air temp = ${temp} C
echo

# Send the temperature value to Zabbix.
# All of the values here are poorly hard coded at this point.
# Once we move these into a project, we should make these configurable variables
zabbix_sender -c /usr/local/etc/zabbix_agentd.conf -s local-hostname -k TA0P -o ${temp}
