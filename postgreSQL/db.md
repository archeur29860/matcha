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

## var

|Critère|Clé primaire UUID | Clé primaire BIGINT (Identity)|
| --- | --- | --- |
|Sécurité|Excellente Impossible de deviner les autres ID (évite le scraping).|Faible. Les ID séquentiels exposent le volume de données.|
|Systèmes distribués|Idéal. Les ID peuvent être générés côté client ou sur plusieurs serveurs sans conflit.|Difficile. Nécessite un serveur centralisé pour éviter les doublons.StockageMoins efficace (16 octets).Très efficace (8 octets).|

## Documentation

https://www.postgresql.org/docs/current/datatype-enum.html
https://www.postgresql.org/docs/current/sql-insert.html