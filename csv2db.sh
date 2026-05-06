# This script
# Extracts data from /etc/passwd file into a CSV file.

# The csv data file contains the user name, user id and
# home directory of each user account defined in /etc/passwd

# Transforms the text delimiter from ":" to ",".
# Loads the data from the CSV file into a table in PostgreSQL database.

echo "Starting Extracting Data"
cut -d":" -f1,3,6 /etc/passwd > extracted-data.txt
echo "Finished Extracting"

echo "Starting Transforming Data"
tr [":"] [","] < extracted-data.txt > transformed-data.csv
echo "Finished Transforming"

# Load phase
echo "Loading data"
# Set the PostgreSQL password environment variable.
# Replace <yourpassword> with your actual PostgreSQL password.
export PGPASSWORD=MMp4TsY81XukAto3uecxXQpk
# Send the instructions to connect to 'template1' and
# copy the file to the table 'users' through command pipeline.
echo "\c template1;\COPY users  FROM '/home/project/transformed-data.csv' DELIMITERS ',' CSV;" | psql --username=postgres --host=postgres
echo "Finished Loading"