```sh
docker-compose up -d
```

```sh
docker-compose exec kafka kafka-topics --create --topic orders --bootstrap-server kafka:29092 --partitions 1 --replication-factor 1
docker-compose exec kafka kafka-topics --create --topic payments --bootstrap-server kafka:29092 --partitions 1 --replication-factor 1
```