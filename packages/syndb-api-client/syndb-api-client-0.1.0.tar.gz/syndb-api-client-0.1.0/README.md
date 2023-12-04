# SynDB FastAPI for user management

Authentication utilizes oAuth + JWT.

## Contribute

When testing with docker locally and there is a change in `poetry.lock`, generate/refresh `requirements.txt` by running:
```shell
cd ./package
poetry export --without-hashes > requirements.txt
```

### Migrate DB changes to production
Setup port-forwarding to the database:
```shell
just dbpf
```

Create alembic revision:
```shell
just arevision
```
Then:
```shell
just aupgrade
```