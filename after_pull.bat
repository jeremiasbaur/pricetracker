psql -U postgres -c "drop database pricetracker_database;"
psql -U postgres -c "create database pricetracker_database with owner postgres encoding = 'UTF8';"
psql -U postgres -d pricetracker_database -f ./DatabaseDumps/pricetracker_database.sql
pause