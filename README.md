# Send temperature

Shell script to send temperature statistics from a Mac to Zabbix

## Dependencies
* Python & [Fabirc](http://www.fabfile.org/)
* A compilied version of the command line smc tool
* [Zabbix](http://www.zabbix.com/)

## Install
### On your Zabbix server

Configure your Zabbix server to accept a custom data point.

1. Configuration > Hosts
1. Create a new item in the host you will be monitoring.
1. Name = Ambient air temperature
1. Type = Zabbix trapper
1. This script will send that data through using `TA0P` as the key.
1. Type of information = Numeric (float)
1. Units = C
1. All other fields are optional

### On the host
Do this on the Mac that you will be monitoring.

1. Install Python and [Fabric](http://www.fabfile.org/installing.html).
1. [Install the Zabbix agent](https://github.com/scimusmn/zabbix_agent_setup) and configure it with your Zabbix server information.
1. `git clone https://github.com/scimusmn/send-temperature.git`
1. `cd send-temperature`
1. `fab install`
