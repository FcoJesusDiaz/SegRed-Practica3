#!/bin/bash

shopt -s extglob
rm -r database/!(README.md)

cat /dev/null > shadow.txt
