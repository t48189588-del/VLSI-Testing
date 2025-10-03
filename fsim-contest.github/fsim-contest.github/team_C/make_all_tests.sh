#!/bin/sh

for i in data.nogit/*.bench
do
  python 2_make_random_tests_2_teamC.py -i $i
done