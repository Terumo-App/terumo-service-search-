host_volume=C:/Users/Maods/Documents/Development/Mestrado/terumo/apps/terumo-model-binary-glomerulus-hypercellularity/data/raw/
container_volume=/src/db/

docker run --name terumo-service-search-monolith \
            --rm \
            -p5000:5000 \
            -v $host_volume:$container_volume \
            terumo-service-search-monolith 