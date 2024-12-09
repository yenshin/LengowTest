# DB
.PHONY: create-db
create-db:
	docker exec lengow-test-db psql -U dev -d postgres -f /scripts/create_db.sql -v db="lengowtest_v20241208"
	$(CONTAINER_EXECUTOR) alembic upgrade head

.PHONY: create-db
reset-db:
	docker exec lengow-test-db psql -U dev -d postgres -f /scripts/reset_db.sql -v db="lengowtest_v20241208"
	$(CONTAINER_EXECUTOR) alembic upgrade head

.PHONY: downgrade-db
downgrade-db:
	$(CONTAINER_EXECUTOR) alembic downgrade -1

.PHONY: migrate-db
migrate-db:
	$(CONTAINER_EXECUTOR) alembic upgrade head

.PHONY: autogenerate-migration
autogenerate-migration:
	$(CONTAINER_EXECUTOR) alembic revision --autogenerate -m $(revision_message)