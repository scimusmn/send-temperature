"""Recipes to send computer temperature data to Zabbix"""

from fabric.api import abort, hide, local, settings, task
from contextlib import contextmanager
import re


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
    TA0P_output = local(smc + ' -k TA0P -r', True)

    try:
        regex = re.compile('\] .([0-9.]*) \(')
        temperature = regex.search(TA0P_output).group(1)
    except AttributeError:
        abort('Couldn\'t exctract the temperature from smc\'s output: ' +
              TA0P_output)

    zabbix_config = '/usr/local/etc/zabbix_agentd.conf'
    zabbix_hostname = 'bkennedy-mbp'
    local('zabbix_sender -c ' + zabbix_config + ' -s ' + zabbix_hostname +
          ' -k TA0P -o ' + temperature)
