https://fastapi.tiangolo.com/deployment/docker/#docker-image-with-poetry

To fire up this project use 
```
docker compose up 
```

To check redis database state use 
```
docker exec -it keywords-counter_redis_1 exec redis-cli
```

After docker compose up you can see documentation here `localhost:8080/redoc`

Or send test request
```
# count keywords 
curl -X POST http://localhost:8080/count-keywords -H "Content-Type: application/json" -d '{
  "text": "hello world hello world",
  "keyword": "hello"
}'
# check keyword count
curl -X POST http://localhost:8080/keyword -H "Content-Type: application/json" -d '{"keyword": "hello"}'
# check status of request 
curl -X POST http://localhost:8080/request-status -H "Content-Type: application/json" -d '{
  "rid": "string"
}'
```

here you can find cool trick for stress test like this 
```
# in first terminal
kubectl run -i --tty load-generator2 --rm --image=busybox:1.28 --restart=Never -- /bin/sh -c "while sleep 0.01; do wget -q -O- http://restapi/health; done"
```

```
# in second terminal
kubectl get hpa restapi-hpa --watch
```

https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale-walkthrough/