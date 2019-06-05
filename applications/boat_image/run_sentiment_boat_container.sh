docker run --name boat_container --network=host -it -v /var/run/docker.sock:/var/run/docker.sock -v /tmp:/tmp boat_image:sentiment

# docker exec -it boat_container curl -X GET 127.0.0.1:8080
# docker exec -it boat_container curl -X GET 127.0.0.1:8081
# docker exec -it boat_container curl -X GET 127.0.0.1:8082
# docker exec -it boat_container curl -X GET 127.0.0.1:8080/status
# docker exec -it boat_container curl -X GET 127.0.0.1:8081/status
# docker exec -it boat_container curl -X GET 127.0.0.1:8082/status
# docker exec -it boat_container curl -X POST -d '{ "input": "1" }' --header "Content-Type:application/json" 127.0.0.1:8080/predict
# docker exec -it boat_container curl -X POST -d '{ "input": "2" }' --header "Content-Type:application/json" 127.0.0.1:8081/predict
# docker exec -it boat_container curl -X POST -d '{ "input": "3" }' --header "Content-Type:application/json" 127.0.0.1:8082/predict
 