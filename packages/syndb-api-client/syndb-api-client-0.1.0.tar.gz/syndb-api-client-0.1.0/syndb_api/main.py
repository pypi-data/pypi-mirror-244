import logging
from contextlib import asynccontextmanager
from time import sleep

from brotli_asgi import BrotliMiddleware
from cassandra.cluster import NoHostAvailable
from fastapi import FastAPI
from sqlalchemy.exc import IntegrityError
from starlette.responses import RedirectResponse
from syndb_cassandra.workflow.datastax import create_syndb_tables, driver_connect
from syndb_cassandra.workflow.rs import create_connection

from syndb_api import IN_CLUSTER, package_version
from syndb_api.database.setup import setup_postgres
from syndb_api.neurodata.router import neurodata_router
from syndb_api.settings.constant import settings
from syndb_api.user.router import user_router

logging.basicConfig(
    level=logging.DEBUG if settings.debug else logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    if settings.debug
    else "%(asctime)s - %(name)s - %(message)s",
)

logger = logging.getLogger(__name__)
logger.debug("DEBUG mode detected, hope this is not production!")


@asynccontextmanager
async def fastapi_app_lifespan(fastapi_app: FastAPI):
    if not IN_CLUSTER:
        try:
            await setup_postgres()
            logger.info("Migrated schema to PostgresSQL")
        except IntegrityError:
            pass

    logger.debug("Establishing connection with Scylla DB")
    while True:
        try:
            session = driver_connect()
            break
        except NoHostAvailable:
            sleep(2)
            logger.info("Waiting for Scylla DB to come online...")

    logger.info("Connection to Scylla DB established")

    if not IN_CLUSTER:
        logger.info("Synchronized the SynDB data model to Scylla DB")
        create_syndb_tables(session)

    session.shutdown()
    del session

    connection = create_connection(settings.scylla_url)
    fastapi_app.state.scylla = connection
    await connection.startup()

    if not IN_CLUSTER:
        logger.info(f"Path to swagger docs: http://{settings.host_path}/docs")

    try:
        yield
    finally:
        await connection.shutdown()


app = FastAPI(
    title="Synapse DB",
    debug=settings.debug,
    version=package_version,
    root_path=settings.app_root_path,
    openapi_url="/openapi.json",
    lifespan=fastapi_app_lifespan,
)

app.add_middleware(BrotliMiddleware)

app.include_router(user_router, prefix="/user")
app.include_router(neurodata_router, prefix="/neurodata")


@app.get("/")
async def redirect():
    return RedirectResponse("/docs")


if __name__ == "__main__":
    from uvicorn import run

    run(
        "main:app",
        host=settings.app_host,
        port=settings.app_host_port,
        log_level="debug" if settings.debug else "info",
    )
