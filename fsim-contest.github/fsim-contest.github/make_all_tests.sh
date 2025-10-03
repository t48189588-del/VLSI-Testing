#!/bin/sh

for i in data.nogit/*.bench
do
  python 2_make_random_tests.py -i $i
done