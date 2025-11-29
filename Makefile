
run-server-1:
	go run ./cmd/server_http/main.go -port 8070

run-server-2:
	go run ./cmd/server_http/main.go -port 8071

docker-nginx-up:
	docker-compose -f ./services/nginx/docker-compose.yml up -d

docker-nginx-down:
	docker-compose -f ./services/nginx/docker-compose.yml down

docker-nginx-restart: docker-nginx-down docker-nginx-up

curl-server:
	curl http://localhost:8070/info

curl-nginx:
	curl http://localhost:8080/serv #widok zdefiniowany w nginx.conf

curl-nginx-lb:
	curl http://localhost:8080/lb/info #proxy obslugiwane przez nginx z load balancingiem