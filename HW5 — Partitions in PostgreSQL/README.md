0. Start 3 instances of postgres in docker

```sh
docker compose up -d
```

1. Enter `postgres2`:
	```sh
	docker exec -it postgres2 psql -U user -d shard2
	```

	Create a table:

	```pgsql
	CREATE TABLE users (
	  id SERIAL PRIMARY KEY,
	  name TEXT,
	  age INT
	);
	\q
	```

2. Enter `postgres3`:
	```sh
	docker exec -it postgres3 psql -U user -d shard2
	```

	Create a table:

	```pgsql
	CREATE TABLE users (
	  id SERIAL PRIMARY KEY,
	  name TEXT,
	  age INT
	);
	\q
	```

3. Enter `postgres1`:

	```sh
	docker exec -it postgres1 psql -U user -d shard1
	```

	Enable `postgres_fdw` extension:

	```pgsql
	-- enable extension
	CREATE EXTENSION IF NOT EXISTS postgres_fdw;

	-- create servers
	CREATE SERVER shard2 FOREIGN DATA WRAPPER postgres_fdw
	  OPTIONS (host 'postgres2', port '5432', dbname 'shard2');

	CREATE SERVER shard3 FOREIGN DATA WRAPPER postgres_fdw
	  OPTIONS (host 'postgres3', port '5432', dbname 'shard3');

	-- user mappings
	CREATE USER MAPPING FOR user SERVER shard2
	  OPTIONS (user 'user', password 'password');

	CREATE USER MAPPING FOR user SERVER shard3
	  OPTIONS (user 'user', password 'password');
	```

	Create partitioned table:
	```pgsql
	CREATE TABLE users_all (
	  id SERIAL,
	  name TEXT,
	  age INT
	) PARTITION BY RANGE (age);

	-- local partition (age < 30)
	CREATE TABLE users_p1 PARTITION OF users_all
	  FOR VALUES FROM (0) TO (30);

	-- foreign partitions
	CREATE FOREIGN TABLE users_p2 (
	  id SERIAL,
	  name TEXT,
	  age INT
	) SERVER shard2 OPTIONS (table_name 'users');

	ALTER TABLE users_all ATTACH PARTITION users_p2
	  FOR VALUES FROM (30) TO (60);

	CREATE FOREIGN TABLE users_p3 (
	  id SERIAL,
	  name TEXT,
	  age INT
	) SERVER shard3 OPTIONS (table_name 'users');

	ALTER TABLE users_all ATTACH PARTITION users_p3
	  FOR VALUES FROM (60) TO (120);

	\q
	```

4. Write data on `postgres1`:
	```sh
	docker exec -it postgres1 psql -U user -d shard1
	```

	```pgsql
	INSERT INTO users_all (name, age) VALUES ('Alice', 25);
	INSERT INTO users_all (name, age) VALUES ('Bob', 45);
	INSERT INTO users_all (name, age) VALUES ('Charlie', 70);
	```

4. Read data from `postgres1`:
	```sh
	docker exec -it postgres2 psql -U user -d shard2 -c "SELECT * FROM users;"
	```

	```sh
	docker exec -it postgres3 psql -U user -d shard3 -c "SELECT * FROM users;"
	```

	```sh
	docker exec -it postgres1 psql -U user -d shard1 -c "SELECT * FROM users_p1;"
	```

5. Finish
	```sh
	docker-compose down -v
	```
