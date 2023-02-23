# Infrastructure

As mentioned in the general introduction, we are sharing the environment that we used for our hackathon, that is the Weaviate DB including the collected data. With it, you can either query the Weaviate DB directly using GraphQL, or by using a Jupyter notebook.

The dashboard GUI, which is under development, isn't shared, nor is the whole pipeline. Please contact us if you are interested to learn more.

## Prerequisite

As a prerequisite, build the `jupyter-weaviate-interface`.

## Run the environment

To run the hackathon environment, please start all services using Docker compose, either via the Docker GUI or the command line:

```bash
docker compose up -d
```

## Install the data

Import the data into Weaviate using the following command...

## Backups

The Weaviate database can be backed up to the [file system](https://weaviate.io/developers/weaviate/current/configuration/backups.html#filesystem) by setting the appropriate environment properties in the docker compose file. In particular, you need to set the `BACKUP_FILESYSTEM_PATH: /tmp/weaviate` in the Weaviate environment properties, and also make sure that this folder is mapped in your volume settings to a local folder (otherwise the backup is stored inside the container). For example, use the following volume settings: `- /tmp/weaviate:/tmp/weaviate` in order to create a backup in the `/tmp/weaviate` folder.

You can trigger a backup using `curl`, e.g.

```bash
curl -X POST -H "Content-Type: application/json" -d '{ "id": "icemYYYYMMDDHHmmss" }' http://localhost:8888/v1/backups/filesystem

# Check the status
curl --location --request GET 'http://localhost:8888/v1/backups/filesystem/icemYYYYMMDDHHmmss'

# Restore a backup
curl --location --request POST 'http://localhost:8888/v1/backups/filesystem/icemYYYYMMDDHHmmss/restore' --header 'Content-Type: application/json' --data-raw '{}'

# Check the size
du -sh /tmp/weaviate/icemYYYYMMDDHHmmss/

# And tar/compress it
tar -zcvf icem20221110110000.tar.gz /tmp/weaviate/icemYYYYMMDDHHmmss/
```
