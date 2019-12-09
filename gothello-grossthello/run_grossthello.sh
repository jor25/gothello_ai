#!/bin/bash 
for i in $(seq 1000)
do
    java Grossthello white localhost 0 3
    echo -----------------------------
done

