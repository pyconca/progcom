# If the migration with Docker does not work, try to use --privileged.
migration-pause:
	sleep 20

migration:
	docker run \
		-it --rm \
		--network container:psqldb \
		-v $$(pwd):/opt \
		postgres \
		bash -c "psql -U test -W --host psqldb --port 5432 -f /opt/database.sql test && psql -U test -W --host psqldb --port 5432 -f /opt/tables.sql progcom"

dev-db:
	docker-compose -f docker/dev.yml up -d psqldb

dev-db-reset:
	docker-compose -f docker/dev.yml kill psqldb
	docker-compose -f docker/dev.yml rm -f psqldb
