#! /bin/bash
echo "database" | cut -c1-4
echo "database" | cut -c5-8
echo "database" | cut -c1,5

cut -d":" -f1 /etc/passwd
cut -d":" -f1,3,6 /etc/passwd
cut -d":" -f3-6 /etc/passwd
