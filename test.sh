echo "Choose an option for the database:"
echo "(1) - Create a local database."
echo "(2) - Connect to some existing database."
DB_CHOICE=""
while read DB_CHOICE
do
    if [ "$DB_CHOICE" -eq "1" ] || [ "$DB_CHOICE" -eq "2" ]; then
      break
    else
        echo "Choose an option for the database:"
        echo "(1) - Create a local database."
        echo "(2) - Connect to some existing database."
    fi
done