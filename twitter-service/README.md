# Twitter service

A service that collects messages from Twitter and publishes them to Kafka.

## Environment variables

| Variable        | Default         | Description                          |
|-----------------|-----------------|--------------------------------------|
| KAFKA_HOST      | 127.0.0.1:3501  |                                      |
| SCHEMA_REGISTRY | 127.0.0.1:3502  |                                      |
| CLIENT_ID       | twitter_service |                                      |
| CONSUME         | config          |                                      |
| PRODUCE         | article_raw_xx  |                                      |
| SLEEP           | 25              | Before running sleep time in seconds |
