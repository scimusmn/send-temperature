"""Recipes to send computer temperature data to Zabbix"""

from fabric.api import abort, hide, env, local, settings, task
from contextlib import contextmanager
import re
import os
import time


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


def get_launch_script_path():
    """Get the path of the launchd script for this process on this system
    """
    launch_script = (os.sep + 'Users' + os.sep +
                     env.user + os.sep +
                     'Library' + os.sep +
                     'LaunchAgents' + os.sep +
                     'org.smm.send-temperature.plist'
                     )
    return launch_script


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


@task
def install():
    """Install this script on OSX. Use launchd to run script repeatadly
    """
    # Get Fabric path
    fab = which('fab')
    if fab is False:
        abort("Something is wrong. I can't find the full path to Fabric.")

    launchd_template = os.path.join(
        os.path.dirname(__file__),
        "launchd/org.smm.send-temperature.plist"
    )

    with _mute():
        user_path = local('echo $PATH', True)

    with open(launchd_template, "r") as sources:
        lines = sources.readlines()
    launch_script = get_launch_script_path()
    with open(launch_script, "w") as sources:
        for line in lines:
            line = re.sub(
                r'<string>fab</string>',
                '<string>' + fab + '</string>',
                line)
            line = re.sub(
                r'<string>path</string>',
                '<string>' + user_path + '</string>',
                line)
            line = re.sub(
                r'<string>send-temperature</string>',
                '<string>' + os.path.dirname(__file__) + '</string>',
                line)
            sources.write(line)

    # Reload the plist, incase it's already been setup.
    # This makes the process idempotent.
    with settings(warn_only='true'):
        local('launchctl unload ' + launch_script)
    time.sleep(3)
    local('launchctl load ' + launch_script)


@task
def uninstall():
    """Unload and remove the launchd script that keeps this script running
    """
    launch_script = get_launch_script_path()
    with settings(warn_only='true'):
        local('launchctl unload ' + launch_script)
        local('rm ' + launch_script)
