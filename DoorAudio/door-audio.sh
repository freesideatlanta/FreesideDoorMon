#!/bin/sh

### BEGIN INIT INFO
# Provides:          3dhost
# Required-Start:    $remote_fs $syslog
# Required-Stop:     $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Put a short description of the service here
# Description:       Put a long description of the service here
### END INIT INFO

. /lib/lsb/init-functions

do_start () {
    log_daemon_msg "Starting system 3dhost daemon"
    start-stop-daemon --start --pidfile /var/run/3dhost.pid --make-pidfile --user root --chuid root --startas /usr/bin/python -- /usr/local/bin/3dhost/3dhost.py
    log_end_msg $?
}
do_stop () {
    log_daemon_msg "Stopping system 3dhost daemon"
    start-stop-daemon --stop --pidfile /var/run/3dhost.pid --retry 10
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
        status_of_proc 3dhost python && exit 0 || exit $?
        ;;

    *)
        echo "Usage: /etc/init.d/3dhost.sh {start|stop|restart|status}"
        exit 1
        ;;

esac
exit 0
