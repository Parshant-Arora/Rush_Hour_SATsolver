#! /bin/bash

for i in 1 2 3 .. 5
do	
	echo $i 
	python3 generator.py foo.txt

	python3 rush_hour.py foo.txt > bar.txt

	python3 simulate.py foo.txt bar.txt
done	
