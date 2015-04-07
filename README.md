# Send temperature

Shell script to send temperature statistics from a Mac to Zabbix

## Dependencies
* Python & [Fabirc](http://www.fabfile.org/)
* A compilied version of the command line smc tool
* [Zabbix](http://www.zabbix.com/)
  * A remote Zabbix server
  * A local zabbix agentd (this gives us the zabbix_sender command)
