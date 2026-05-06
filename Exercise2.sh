#! /bin/bash

echo "Shell Scripting" | tr "[a-z]" "[A-Z]"
echo "Shell Scripting" | tr "[:lower:]" "[:upper:]"
echo "Shell Scripting" | tr "[A-Z]" "[a-z]"

ps | tr -s " "

echo "My login pin is 5634" | tr -d "[:digit:]"
