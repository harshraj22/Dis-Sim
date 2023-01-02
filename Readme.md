
## Intro:
Dis-Sim is a Microservices architecture based distributed image similarity measuring system. It uses asynchronous message queue to communicate across microservices. Its distributed architecture makes it highly scalable and fault tolerant.
It has a built in data monitoring and analytics service which uses Kafka as a message broker, and sqlite3 as a database.

![architecture](https://user-images.githubusercontent.com/46635452/210266686-16c83011-6351-4877-b2dc-f2a93abb3fe6.png)



### Demo:
![streamlit-frontend-2022-06-08-16-06-21](https://user-images.githubusercontent.com/46635452/210266742-a1f5cc31-977c-4e5c-8f8b-5ec2263d4c62.gif)


### Getting started:
1. Run `docker-compose pull && docker-compose up ` to pull and start all the containers. <details> <summary> Build from source: </summary> `docker-compose up --build ` to build from the source, and not use the already built image from dockerhub. </details>
2. Open the browser and navigate to `localhost:8501`. Note that `8501` is the port specified in the dockerfile of the `frontend` service (`src/frontend/Dockerfile`).
3. Use the existing credentials `username: test, password: test`. Would be soon adding frontend to register new user.


<strong>Note:</strong> Since there are multiple services spinning up, it would take a little longer for all the services to start up before you can start playing with the similarity service. The images are large, and a good internet connection is required. You can expect the whole service to spin up within 5 minutes.


### Using custom similarity measurer:
Adding a custom similarity measurer is as simple as overwriding the `similarity` function in the `src/similarity/models` module.
```python
# import your new similarity measurer

from my_similarity_measurer import MySimilarityMeasurer
```

```python
# add your new similarity measurer in similarity method

@app.task
def similarity(img1, img2) -> float:
    ...

    score = MySimilarityMeasurer().similarity(img1, img2)
    return score
```

Make sure to add the dependencies of your new similarity measurer in `src/similarity/requirements.txt`

### Benchmarks:
- Load Testing: [here](./test/load_test)


### References:
- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Streamlit](https://streamlit.io/)
- [Celery](https://celery.readthedocs.io/en/latest/)
- [Redis](https://redis.io/)
- [Kafka](https://medium.com/swlh/understanding-kafka-a-distributed-streaming-platform-9a0360b99de8)

- [Microservices Architecture](https://en.wikipedia.org/wiki/Microservice)
- [Message Queue](https://en.wikipedia.org/wiki/Message_queue)
 

### Further Reading:
- [Naming Release Versions](https://py-pkgs.org/07-releasing-versioning.html#version-numbering)
