#!/bin/sh

### BEGIN INIT INFO
# Provides:          door-audio
# Required-Start:    $remote_fs $syslog
# Required-Stop:     $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Put a short description of the service here
# Description:       Put a long description of the service here
### END INIT INFO

. /lib/lsb/init-functions

do_start () {
    log_daemon_msg "Starting system door-audio daemon"
    start-stop-daemon --start --background --pidfile /var/run/door-audio.pid --make-pidfile --user root --chuid root --startas /usr/bin/python -- /usr/local/bin/FreesideDoorMon/DoorAudio/DoorAudio.py
    log_end_msg $?
}
do_stop () {
    log_daemon_msg "Stopping system door-audio daemon"
    start-stop-daemon --stop --pidfile /var/run/door-audio.pid --retry 10
    log_end_msg $?
}

case "$1" in

    start|stop)
        do_${1}
        ;;

    restart|reload|force-reload)
        do_stop
        do_start
        ;;

    status)
        status_of_proc door-audio python && exit 0 || exit $?
        ;;

    *)
        echo "Usage: /etc/init.d/door-audio.sh {start|stop|restart|status}"
        exit 1
        ;;

esac
exit 0
