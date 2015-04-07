"""Recipes to send computer temperature data to Zabbix"""

from fabric.api import hide, local, settings, task
from contextlib import contextmanager


def _header(txt):
    """Decorate a string to make it stand out as a header. """
    wrapper = """
-------------------------------------------------------------------------------
"""
    return wrapper.strip() + "\n" + txt + "\n" + wrapper.strip()


@contextmanager
def _mute():
    """Run a fabric command without reporting any responses to the user. """
    with settings(warn_only='true'):
        with hide('running', 'stdout', 'stderr', 'warnings'):
            yield


def get_smc():
    """Get the path to the smc command
    """
    path = local('which smc', True)
    return path


@task
def send():
    """Send temperature data to the Zabbix server
    """
    # Use the smc command line tool to read the TA0P sensor
    # This sensor is the Ambient Air temperature
    # Data is in Celsius
    # Use sed and perl to parse the value into only the digits
    print
    print 'Execute smc'
    with _mute():
        smc = get_smc() + ' -l'
    print smc
    local(smc)
    # local('brew install zabbix --agent-only')

    # temp="$(smc -k TA0P -r | sed 's/.*bytes \(.*\))/\1/' | sed 's/\([0-9a-fA-F]*\)/0x\1/g' | perl -ne 'chomp; ($low,$high) = split(/ /); print(((hex($low)*256)+hex($high))/4/64);')"

    # echo Ambient air temp = ${temp} C
    # echo

    # Send the temperature value to Zabbix.
    # All of the values here are poorly hard coded at this point.
    # Once we move these into a project, we should make these
    # configurable variables
    # zabbix_sender
    # -c /usr/local/etc/zabbix_agentd.conf -s local-hostname -k TA0P -o ${temp}
