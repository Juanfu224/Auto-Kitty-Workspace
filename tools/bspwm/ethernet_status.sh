#!/bin/sh
 
echo "%{F#2495e7} %{F#ffffff}$(/usr/sbin/ifconfig wlp1s0 | grep "inet " | awk '{print $2}')%{u-}"
