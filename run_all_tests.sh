#!/bin/bash

test_info_file_dir=$(cd `dirname $1` && pwd)
test_info_file=$test_info_file_dir/`basename $1`

cd testcases
for i in */run_test
do
	if [ -x $i ] && ! $i $test_info_file
	then
		exit 1
	fi
done
