#!/bin/bash

# Fix terminal. 
echo "LANG=en_US.UTF-8" > /etc/default/locale
apt-get install $(grep -vE "^\s*#" packages.lst  | tr "\n" " ") -y
