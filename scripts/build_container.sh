# pipenv requirements > requirements.txt
docker build -t terumo-service-search-monolith .

docker tag terumo-service-search-monolith terumoapp/terumo-service-search-monolith:latest