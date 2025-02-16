#!/bin/bash
cd /root/cpu2006
source shrc

echo $$ > /repabp/test/tasks
echo enable > /sys/kernel/debug/repabp/control
runspec --action=run --config=my.cfg --size=ref --iterations=1 --tune=base --nobuild --noreportable $1
echo disable > /sys/kernel/debug/repabp/control