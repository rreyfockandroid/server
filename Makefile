
prun-server-1:
	python plib/main.py -port=8060

run-server-1:
	go run ./cmd/server_http/main.go -port 8070

run-server-2:
	go run ./cmd/server_http/main.go -port 8071

docker-nginx-up:
	docker-compose -f ./services/nginx/docker-compose.yml up -d

docker-nginx-down:
	docker-compose -f ./services/nginx/docker-compose.yml down

docker-nginx-restart: docker-nginx-down docker-nginx-up

docker-nginx-log:
	docker logs nginx_server

curl-server:
	curl http://localhost:8070/info

curl-nginx:
	curl http://localhost:8080/serv #widok zdefiniowany w nginx.conf

curl-nginx-dir:
	curl http://localhost:8080/a/b/c/ #statyczne pliki obslugiwane przez nginx

curl-nginx-lb:
	curl http://localhost:8080/lb/info #proxy obslugiwane przez nginx z load balancingiem

ca-gen-py:
	openssl genrsa -out ./services/nginx/storage/certs/rootCA.key 4096
	openssl req -x509 -new -nodes \
		-key ./services/nginx/storage/certs/rootCA.key \
		-sha256 -days 365 \
		-subj "/C=PL/ST=pomorskie/L=gdansk/O=home/CN=server.py.pl CA" \
		-out ./services/nginx/storage/certs/rootCA.crt

mkdir-private:
	mkdir -p services/storage/certs/private

cert-gen-py: mkdir-private
	openssl genrsa -out ./services/nginx/storage/certs/private/nginx-selfsigned.key 2048

	openssl req -new \
		-key ./services/nginx/storage/certs/private/nginx-selfsigned.key \
		-subj "/C=PL/ST=pomorskie/L=gdansk/O=home/CN=server.py.pl" \
		-out ./services/nginx/storage/certs/server.csr

	echo "authorityKeyIdentifier=keyid,issuer\nbasicConstraints=CA:FALSE\nkeyUsage=digitalSignature, keyEncipherment\nsubjectAltName=DNS:server.py.pl" > ./services/nginx/storage/certs/server.ext

	openssl x509 -req \
		-in ./services/nginx/storage/certs/server.csr \
		-CA ./services/nginx/storage/certs/rootCA.crt \
		-CAkey ./services/nginx/storage/certs/rootCA.key \
		-CAcreateserial \
		-out ./services/nginx/storage/certs/nginx-selfsigned.crt \
		-days 365 -sha256 \
		-extfile ./services/nginx/storage/certs/server.ext

ca-gen-go:
	openssl genrsa -out ./services/nginx/storage/certs/rootCA_go.key 4096
	openssl req -x509 -new -nodes \
		-key ./services/nginx/storage/certs/rootCA_go.key \
		-sha256 -days 365 \
		-subj "/C=PL/ST=pomorskie/L=gdansk/O=home/CN=server.go.pl CA" \
		-out ./services/nginx/storage/certs/rootCA_go.crt

cert-gen-go: mkdir-private
	openssl genrsa -out ./services/nginx/storage/certs/private/nginx-go-selfsigned.key 2048

	openssl req -new \
		-key ./services/nginx/storage/certs/private/nginx-go-selfsigned.key \
		-subj "/C=PL/ST=pomorskie/L=gdansk/O=home/CN=server.go.pl" \
		-out ./services/nginx/storage/certs/server_go.csr

	echo "authorityKeyIdentifier=keyid,issuer\nbasicConstraints=CA:FALSE\nkeyUsage=digitalSignature, keyEncipherment\nsubjectAltName=DNS:server.go.pl" > ./services/nginx/storage/certs/server_go.ext

	openssl x509 -req \
		-in ./services/nginx/storage/certs/server_go.csr \
		-CA ./services/nginx/storage/certs/rootCA_go.crt \
		-CAkey ./services/nginx/storage/certs/rootCA_go.key \
		-CAcreateserial \
		-out ./services/nginx/storage/certs/nginx-go-selfsigned.crt \
		-days 365 -sha256 \
		-extfile ./services/nginx/storage/certs/server_go.ext

cert-gen-dh:
	sudo openssl dhparam -out ./services/nginx/storage/certs/dhparam.pem 2048

domains-add:
	echo "127.0.0.1	server.py.pl server.go.pl" | sudo tee -a /etc/hosts > /dev/null