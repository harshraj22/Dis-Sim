## Running Load Test
1. Spin up all the servers using `docker-compose`.
2. Run load test using command line: `locust --headless --users 100 --spawn-rate 1 -H http://0.0.0.0:8001`. Note `8001` is the port for api end point specified in the corresponding docker file (`src/api/Dockerfile`)
3. You can use the GUI version using `loctus`. Make sure you are in the directory `test/load_test/` as `locustfile.py` is present there.

Note: It is advisable to run the heavy tests on isolated environments like github codespaces (and not on your local machine).


<br>

## Benchmarks:
<img width="1257" alt="image" src="https://user-images.githubusercontent.com/46635452/173183269-3c817544-8b8e-4dfa-96f3-9c903579325f.png">
         

<br>          

## References:        

- Locust: [docs](https://docs.locust.io/en/stable/what-is-locust.html)        
- Load Testing: 