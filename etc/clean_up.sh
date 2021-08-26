#!/bin/bash
set -euo pipefail

clean_journal_logs() {
    # cleans journal logs
    /bin/rm /var/log/clean_up.log
    /bin/rm /var/log/grive.log
    # rotate the files first so that recent entries are moved to inactive files
    /bin/journalctl --rotate

    # Retain only the past two days:
    /bin/journalctl --vacuum-time=30d

    # Retain only the past 500 MB:
    /bin/journalctl --vacuum-size=500M
    return 0
}

clean_old_snaps() {
    # Removes old revisions of snaps
    /usr/bin/snap list --all | /usr/bin/awk '/disabled/{print $1, $3}' |
        while read snapname revision; do
            /usr/bin/snap remove "$snapname" --revision="$revision"
        done
    return 0
}

clean_apt() {
    # Cleans apt related resources
    /usr/bin/apt-get clean --assume-yes
    /usr/bin/apt-get autoclean --assume-yes
    /usr/bin/apt-get autoremove --purge --assume-yes
    return 0
}

clean_old_kernels() {
    return 0
}

clean_docker() {
    /usr/bin/docker system prune --force --all
    return 0
}

if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 
   exit 1
else
    clean_journal_logs && clean_old_snaps && clean_apt && clean_old_kernels && clean_docker
fi

exit 0
