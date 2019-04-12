psql -U postgres -c "drop database pricetracker_database;"
psql -U postgres -c "create database pricetracker_database with owner postgres encoding = 'UNICODE';"
psql -U postgres -d pricetracker_database -f pricetracker_database.sql
pause