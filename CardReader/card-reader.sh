#!/bin/sh

### BEGIN INIT INFO
# Provides:          card-reader
# Required-Start:    $remote_fs $syslog
# Required-Stop:     $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Put a short description of the service here
# Description:       Put a long description of the service here
### END INIT INFO

. /lib/lsb/init-functions

do_start () {
    log_daemon_msg "Starting system card-reader daemon"
    start-stop-daemon --start --background --pidfile /var/run/card-reader.pid --make-pidfile --user root --chuid root --startas /usr/bin/python -- /usr/local/bin/FreesideDoorMon/CardReader/CardReader.py
    log_end_msg $?
}
do_stop () {
    log_daemon_msg "Stopping system card-reader daemon"
    start-stop-daemon --stop --pidfile /var/run/card-reader.pid --retry 10
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
        status_of_proc card-reader python && exit 0 || exit $?
        ;;

    *)
        echo "Usage: /etc/init.d/card-reader.sh {start|stop|restart|status}"
        exit 1
        ;;

esac
exit 0
