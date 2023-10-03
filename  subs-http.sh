#!/bin/bash
SUBDOMAINS=$(python /opt/Sublist3r/sublist3r.py -d angislist.com)
for sub in $SUBDOMAINS
do
    nmap -p 443 $sub
done

