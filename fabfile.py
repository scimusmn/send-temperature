"""Recipes to send computer temperature data to Zabbix"""

from fabric.api import abort, hide, local, settings, task
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


def which(cmd):
    """Get the path of a command
    """
    with _mute():
        result = local('which ' + cmd, True)
        if result.failed:
            return False
        else:
            return result


@task
def send():
    """Send temperature data to the Zabbix server
    """
    smc = which('smc')
    if smc is False:
        abort("smc is not installed.")

    # Use the smc command line tool to read the TA0P sensor
    # This sensor is the Ambient Air temperature
    # Data is in Celsius
    temp = local(smc + ' -k TA0P -r')
    print temp
    # Use sed and perl to parse the value into only the digits

    # temp="$(smc -k TA0P -r | sed 's/.*bytes \(.*\))/\1/' | sed 's/\([0-9a-fA-F]*\)/0x\1/g' | perl -ne 'chomp; ($low,$high) = split(/ /); print(((hex($low)*256)+hex($high))/4/64);')"

    # echo Ambient air temp = ${temp} C
    # echo

    # Send the temperature value to Zabbix.
    # All of the values here are poorly hard coded at this point.
    # Once we move these into a project, we should make these
    # configurable variables
    # zabbix_sender
    # -c /usr/local/etc/zabbix_agentd.conf -s local-hostname -k TA0P -o ${temp}
