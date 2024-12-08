# DB
.PHONY: create-db
create-db:
	docker exec lengow-test-db psql -U dev -d postgres -f /scripts/create_db.sql -v db="lengowtest_v20241208"
