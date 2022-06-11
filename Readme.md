## Phase 1

### What works ?
- [x] `docker-compose` spins up all the services.
- [x] The services have been tested manually using `localhost:<port>/docs`
- [x] Celery and Redis work as expected.

### ToDo:
- [x] Add a frontend (Streamlit preferably)
- [x] Replace the similarity with actual deep learning model.
- [ ] Make a cookiecutter template for the project.


### Demo:
![myfile](./artifacts/streamlit-frontend-2022-06-08-16-06-21.gif)


### Getting started:
1. Run `docker-compose up --build` to create and start all the containers. (Use `-d` to run in the background)
2. Open the browser and navigate to `localhost:8501`


### Benchmarks:
- Load Testing: [here](./test/load_test)
