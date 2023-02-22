# Text readability service

A service that calculates the readability of text.

## Environment variables

| Variable        | Default                  | Description |
|-----------------|--------------------------|-------------|
| KAFKA_HOST      | 127.0.0.1:3501           |             |
| SCHEMA_REGISTRY | 127.0.0.1:3502           |             |
| CLIENT_ID       | readability_en_service   |             |
| CONSUME         | article_raw_en           |             |
| PRODUCE         | key_value_xx             |             |
