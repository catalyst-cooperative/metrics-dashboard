import os
import sqlalchemy as sa


def get_sql():
    """Connect application to Postgres database with usage metrics.

    Return the sqlalchemy engine, but also the metadata which has all the table defs.

    Since the tables are defined in the ETL repo, we merely reflect them here.

    Uses host/port in development environment, but on Cloud Run we use a Unix
    socket under /cloudsql.

    """
    username = os.getenv("METRICS_DASHBOARD_DB_USERNAME")
    password = os.getenv("METRICS_DASHBOARD_DB_PASSWORD")
    database = os.getenv("METRICS_DASHBOARD_DB_NAME")

    if os.environ.get("IS_CLOUD_RUN"):
        cloud_sql_connection_name = os.environ.get("CLOUD_SQL_CONNECTION_NAME")
        db_uri = f"postgresql://{username}:{password}@/{database}?host=/cloudsql/{cloud_sql_connection_name}"
    else:
        host = os.getenv("METRICS_DASHBOARD_DB_HOST")
        port = os.getenv("METRICS_DASHBOARD_DB_PORT", "5432")
        db_uri = f"postgresql://{username}:{password}@{host}:{port}/{database}"

    engine = sa.create_engine(db_uri)
    metadata = sa.MetaData()
    metadata.reflect(engine)
    return engine, metadata
