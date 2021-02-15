#!/usr/bin/env bash
# Provision a pool, ingress data, run a job,
# and delete job and pool (once the job is completed).
# cli: ./shipyard-driver.sh

scriptdir="$( cd "$(dirname "$0")" ; pwd -P )"
casedir="$( cd "$(dirname "$scriptdir")" ; pwd -P )"

cd $casedir
configdir="config_shipyard"
logdir="log_shipyard"
mkdir -p $logdir

printf "Polling job until tasks are complete ...\n"
shipyard jobs tasks list --configdir=$configdir --poll-until-tasks-complete > $logdir/jobs-monitor.log 2>&1
printf "Deleting pool ...\n"
shipyard pool del --configdir=$configdir --yes > $logdir/pool-del.log 2>&1

printf "Done!\n"
