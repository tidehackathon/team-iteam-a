# Overview of the solution by i-Team A: Disinformation Analyzer

## Problem

Josep Borrell, High Representative/Vice-President, adequately described the problem as follows: _“We have to focus on foreign actors who intentionally, in a coordinated manner, try to manipulate our information environment. We need to work with democratic partners around the world to fight information manipulation by authoritarian regimes more actively. It is time to roll up our sleeves and defend democracy, both at home and around the world.”_ [source: FIMI](https://www.eeas.europa.eu/eeas/1st-eeas-report-foreign-information-manipulation-and-interference-threats_en). So, for this challenge, the focus is on calculating the credibility that a news article or social media message represents true information, and not disinformation.

## Methodology

The methodology has been created by understanding the anatomy of disinformation and misinformation.

### Types of Misinformation and Disinformation

- Fabricated Content: false content;
- Manipulated Content: Genuine information or imagery that has been distorted, e.g. a sensational headline or populist ‘click bait’;
- Imposter Content: Impersonation of genuine sources, e.g. using the branding of an established agency;
- Misleading Content: Misleading information, e.g. comment presented as fact;
- False Context: Factually accurate content combined with false contextual information, e.g. when the headline of an article does not reflect the content;
- Satire and Parody: Humorous but false stores passed off as true. There is no intention to harm but readers may be fooled;
- False Connections: When headlines, visuals or captions do not support the content;
- Sponsored Content: Advertising or PR disguised as editorial content;
- Propaganda: Content used to manage attitudes, values and knowledge;
- Error: A mistake made by established new agencies in their reporting.

In addition to new and more sophisticated ways of manipulating content, there are also a growing number of ways in which social media can be used to manipulate conversations:

- A Sockpuppet is an online identity used to deceive. The term now extends to misleading uses of online identities to praise, defend, or support a person or organization; to manipulate public opinion; or to circumvent restrictions, suspension or an outright ban from a website. The difference between a pseudonym and a sockpuppet is that the sockpuppet poses as an independent third party, unaffiliated with the main account holder. Sockpuppets are unwelcome in many online communities and forums;
- Sealioning is a type of trolling or harassment where people are pursued with persistent requests for evidence or repeated questions. A pretence of civility and sincerity is maintained with these incessant, bad-faith invitations to debate;
- Astroturfing masks the sponsors of a message (e.g. political, religious, advertising or PR organizations) to make it appear as though it comes from grassroots participants. The practice aims to give organizations credibility by withholding information about their motives or  connections;
- Catfishing is a form of fraud where a person creates a sockpuppet or fake identity to target a particular victim on social media. It is common for romance scams on dating websites. It may be done for financial gain, to compromise a victim or as a form of trolling or wish fulfilment.
Understanding the anatomy of fake news, people can detect if a news is true or false. To detect it people are advised to ask 10 questions:

![10 questions to ask](https://user-images.githubusercontent.com/3140667/221019405-bf40d0d0-bd0a-4648-b18f-70644041f642.png)

Therefore, the approach that is followed can be split into 4 stages, and each stage is discussed in more detail below:

1. Collect relevant content.
2. Enrich that content using ML.
3. Add vector embeddings to the content for semantic analysis and store the content.
4. Analyse the content, automatically and/or manually.

Next, the implementation is discussed: it is based on the open source event streaming platform, [Apache Kafka](https://kafka.apache.org), which is used to connect many micro-services that enrich the content. In the context of this hackathon, a part of this solution is shared - the full solution is, in principle, available to NATO-affiliated government organisations, so please reach out to us to discuss it.

Subsequently, the results are explained. Based on the data in this repository, a user can play with the provided content in the database, either by querying it using GraphQL, or by running a Jupyter notebook. In the full solution, a GUI can be used that is more powerful, but not part of the released software (see the comment above).

### Collecting content

![Simplified pipeline](https://user-images.githubusercontent.com/3140667/221025339-e70e38e6-0cdd-4325-a75b-c7ae9d5b6d0e.png)

Analysts are in the best position to determine what information sources contain the most relevant content: RSS feeds, websites, telegram channels, twitter hashtags, etc. They can specify them in the GUI (not included), including their refresh rate. Alternatively, they can upload their own URLs manually or via a script.

The provided dataset contains, for example, data from the provided CSVs, but also from TASS, [EMM (Europe Media Monitor)](https://emm.newsbrief.eu/NewsBrief/clusteredition/en/latest.html), Google News, New York Times, and several others.

When the relevant channels are specified, the configuration is published to Kafka, and the crawlers and scrapers start to collect content. In case of RSS feeds, the RSS crawlers first analyse the RSS feed for new content, and subsequently publish the new article links to Kafka. In the complete framework, there are many scrapers, e.g. for generic websites, dedicated websites, telegram, and twitter. The twitter service, that was developed during the hackathon, is available in the `twitter-service`, and it should provide an example of how easy it is to add a new service. Discovered content, be it text or images, are published by the scrapers to Kafka as well, so the content can be processed in the next stage.

### Processing content
![Simplified sequence diagram of the pipeline](https://user-images.githubusercontent.com/3140667/221022136-1df44456-c6ac-4768-aed2-3b42a36ee1a3.png)

When the article content is available, many NLP microservices start to work in parallel to enrich the retrieved articles. To name a few:

- Language detection & translation using Franc and LibreTranslate
- Summarizing
- Named Entity Recognition (+keywords)
- Geo-tagging
- Face detection
- Sentiment & Emotion score
- Readability score
- Sarcasm/joke score
- Topic detection: Louvain algorithm
- Channel affiliation & credibility
- Semantic word embeddings in Weaviate: `semitechnologies/transformers-inference:sentence-transformers-paraphrase-multilingual-mpnet-base-v2`
- Semantic image embeddings in Weaviate: `semitechnologies/img2vec-pytorch:resnet50`

During this hackathon, we developed the emotion and readability score microservice, which are available in this repository as well.

The outcome of each microservice is, again, published to Kafka, and aggregated in the next stage.

### Storing and semantically embedding content

When the hard work is done, and the articles and tweets are analysed in detail, the results are uploaded to the database. The database that is selected is [Weaviate](https://weaviate.io), which is a so-called vector database. Basically, it not only stores your data, as so many other databases do too, but it first computes a word embedding using a multi-lingual BERT-based NLP transformer-service. This is done for the article as a whole, but also for each paragraph, which enables semantic search and Question & Answer.

In the `infrastructure` folder, you see a complete setup for you to test: it contains the weaviate database service, the transformers for text _and_ images, and a Jupyter notebook service, so you can play with it yourself. Alternatively, you can query the database directly using GraphQL.

### Analysing content

In the final stage, the enriched content is presented to the analyst. A disinformation score is computed based on the computed NLP attributes and the relevancy of an article's content with respect to the current narrative. The analyst can query it using GraphQL or Jupyter Notebooks. See the examples in the folders `infrastructure`, to get everything running locally, and `Jupyter-Weaviate-interface` to build the Jupyter notebook.

![Example of the Weaviate GraphQL interface](https://user-images.githubusercontent.com/3140667/221025672-a4677ae0-ab86-4a6d-8a90-e11b78ecc683.png)
![Example of a Jupyter Notebook](https://user-images.githubusercontent.com/3140667/221025686-3074ec09-46bc-4e73-bfc5-b94981e0fe8d.png)

## Implementation

Our implementation is a microservices-based architecture, where each microservice is connected to Apache Kafka. Kafka acts as the middleware _glue_, connecting all microservices, so they can easily exchange information between each other.

To facilitate deployment, all services are running in Docker: for testing purposes, we run on one or two older Dell desktops with 32Gb but without GPU. All dockerized microservices and other services are connected through Apache Kafka using a single broker.

Only communication to the [Weaviate - vector search engine DB](https://weaviate.io/) is through REST.

Weaviate is configured to vectorize text (i.e. create semantic word embeddings of the whole article and each paragraph), images (so we can recognize similar images), and it includes a Question & Answering service. The latter, for example, can be used to ask a question such as “Who is the current president of the US?”. However, more interestingly, it could also be used to verify the credibility of a news channel: define control questions that you know the answer of, and ask the channel to provide the answers. If there are many wrong answers, you can mark the news channel as untrustworthy. And, of course, this could be automated too.

In the GUI, all saved articles are stored inside a knowledge graph, so we can do graph queries too.  

### Federated analysis & learning

Although our research environment is running standalone, it could also run in a federated context, connecting different organisations. The scraped and enriched articles by organisation A can easily be shared with another Kafka cluster run by organisation B, so it doesn't need to scrape the same websites. In addition, analysist feedback, e.g. the credibility of a news channel or article, can also be shared through Kafka, improving the analysis capability of organisations.

![image](https://user-images.githubusercontent.com/3140667/221024773-ee9221af-6148-41c9-bc28-33fa59c3bd94.png)

Besides federated analysis, the fact that analysist's feedback is stored back in the database, supports learning from examples. AI models can be trained to suggest other disinformation messages, similarly to [ASreview](https://asreview.nl/) that helps researchers quickly discover relevant articles from a list of articles.

### Open source services and NLP models that are used

- [Apache Kafka](https://kafka.apache.org/), [Zookeeper](https://zookeeper.apache.org/) and the [AVRO Schema Registry](https://hub.docker.com/r/confluentinc/cp-schema-registry): All based on the Community Edition supported by [Confluent](https://hub.docker.com/u/confluentinc),
- GUI based on [csNext](https://github.com/TNOCS/csnext).
- Adapters to easily connect to Kafka in Python, [osint-python-test-bed-adapter](https://pypi.org/project/osint-python-test-bed-adapter/), and Node.js, [node-test-bed-adapter](https://www.npmjs.com/package/node-test-bed-adapter).
- Emotion service, based on: [j-hartmann/emotion-english-distilroberta-base · Hugging Face](https://huggingface.co/j-hartmann/emotion-english-distilroberta-base).
- Readability service, based on: [py-readability-metrics · PyPI](https://pypi.org/project/py-readability-metrics/)
- Twitter service, based on: [snscrape · PyPI](https://pypi.org/project/snscrape).
- NER service and keywords service, based on [spacy + English · spaCy Models Documentation](https://spacy.io/models/en) (same for other languages).
- Summary service, based on [sentence-transformers/paraphrase-MiniLM-L6-v2 · Hugging Face](https://huggingface.co/sentence-transformers/paraphrase-MiniLM-L6-v2).
- Translation service, using locally installed and standalone version of [LibreTranslate - Free and Open Source Machine Translation API](https://libretranslate.com/)
- Language service, based on: [franc - npm (npmjs.com)](https://www.npmjs.com/package/franc),
- PDF to tekst, based on: [PyMuPDF · PyPI](https://pypi.org/project/PyMuPDF/).
- Topics service: [graphology-communities-louvain - npm (npmjs.com)](https://www.npmjs.com/package/graphology-communities-louvain).
- Face recognition service, based on: [opencv-python · PyPI](https://pypi.org/project/opencv-python/).
- Telegram service, based on [Telethon · PyPI](https://pypi.org/project/Telethon/).
- Geo-service, based on [geopy · PyPI](https://pypi.org/project/geopy/).

## Screenshots from the Analyst Dashboard

The analyst can search through the enriched articles, either via GraphQL or a Jupyter Notebook, but also through our own GUI.

![Search through relevant articles](https://user-images.githubusercontent.com/3140667/221023416-18c390d2-a56b-4be8-b281-3fd76463c714.png)

![Examine a disinformation narrative](https://user-images.githubusercontent.com/3140667/221023754-1a674b23-f6c6-4d46-8065-cabcdbd06baf.png)

![Explore the results in a cluster diagram](https://user-images.githubusercontent.com/3140667/221023885-79b70504-1277-403e-bab9-96e20575a556.png)

![Or explore the results on the map](https://user-images.githubusercontent.com/3140667/221024044-4ad38a32-e912-40f7-9be8-0f5173aec901.png)





