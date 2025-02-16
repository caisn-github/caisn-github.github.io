#!/bin/bash
cd /root/cpu2006
source shrc

damo record --ops paddr -o damon.data "runspec --action=run --config=my.cfg --size=ref --iterations=1 --tune=base --nobuild --noreportable $1"

damo report heats -i ./damon.data --heatmap ./heatmap.png