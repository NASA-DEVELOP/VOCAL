# Use this command in sqlite3 to generate a script you can use to drop 
# the table of your choice
select 'drop table ' || name || ';' from sqlite_master
    where type = 'table';

# Same as above but for indexes
