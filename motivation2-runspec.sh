#!/bin/bash
cd /root/cpu2006
source shrc

echo $$ > /sys/kernel/debug/memory_detector/pid
runspec --action=run --config=my.cfg --size=ref --iterations=1 --tune=base --nobuild --noreportable $1
