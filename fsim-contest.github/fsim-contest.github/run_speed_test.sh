#!/bin/sh

D=team_C

cd $D

for d in c17 c432 c499 c880 c1355
do
	python 3_stuck_at* data.nogit/$d.bench data.nogit/$d.tests >>run_speed.stdout 2>>run_speed.stderr
done
