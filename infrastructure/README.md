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

Or you can use the provided scripts (`start`, `down`, `stop`).

## Install the data

The Weaviate data was backed up using the following command:

```bash
curl -X POST -H "Content-Type: application/json" -d '{ "id": "tide_hackathon_2023" }' http://localhost:8888/v1/backups/filesystem
```

To import the data into Weaviate use the following command:

```bash
curl -X POST -H "Content-Type: application/json" -d '{ "id": "tide_hackathon_2023" }' http://localhost:8888/v1/backups/filesystem
```

## Querying Weaviate using GraphQL

- Open the [Weaviate console](http://localhost:8000)
- Connect to Weaviate running on `http://localhost:8888`
- Perform some GraphQL queries to get the data

```graphql
{
  Get {
    Article(
      limit: 50
      nearText: {
        concepts: ["NATO is an aggressor"], 
        moveAwayFrom: { concepts: ["EU"], force: 1 }
      }
    ) {
      title
      text
      created
      sourceId
      # metadata
      hasChannel {
        ... on Channel {
          name
          affiliation
          credibility
          influence
          type
          orientation
          kgId
          _additional {
            id
          }
        }
      }
      hasMediaItems {
        ... on MediaItem {
          contentType
          _additional {
            id
          }
          # metadata
          alt
          height
          width
          url
        }
      }
      original
      originalLanguage
      sourceId
      entities
      feedId
      language
      readability
      languageFlags
      type
      pub_date
      url
      updated
      annotations
      commentsCount
      dislikesCount
      likesCount
      viewsCount
      sharesCount
      history
      version
      fear
      joy
      readability
      cred
      disinfoType
      anger
      surprise
      storyId
      storyCount
      cred
      credMan
      sadness
      sarcasm
      _additional {
        id
        distance
        lastUpdateTimeUnix
        creationTimeUnix
        featureProjection {
          vector
          __typename
        }
      }
    }
  }
}
```

Since the Q&A module has been installed, you can also ask it questions, e.g.

```graphql
{
  Get {
    Article(
      ask: {
        question: "Who held a speech in Poland?", 
        properties: ["title", "text"]
      }
    ) {
      title
      _additional {
        answer {
          hasAnswer
          property
          result
          startPosition
          endPosition
        }
      }
    }
  }
}
```

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
