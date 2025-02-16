#!/bin/bash
cd /root/cpu2006
source shrc

echo $$ > /sys/fs/cgroup/memory_detector/test/tasks
echo start > /sys/kernel/debug/memory_detector/control
runspec --action=run --config=my.cfg --size=ref --iterations=1 --tune=base --nobuild --noreportable $1
echo end > /sys/kernel/debug/memory_detector/control

