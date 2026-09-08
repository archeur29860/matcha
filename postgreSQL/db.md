# Data Base

## connection

```bashnull
make postgres
psql -U mon_utilisateur -d ma_base_de_donnees
```

## Show tables

```postgres
\d -- all
\d table_name

```
```SQL
SELECT * FROM users;
```
## Documentation

https://www.postgresql.org/docs/current/datatype-enum.html
https://www.postgresql.org/docs/current/sql-insert.html