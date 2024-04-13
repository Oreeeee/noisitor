import psycopg


def get_connection(
    port: int, password: str, host: str = "postgres-db"
) -> psycopg.Connection:
    # TODO: Replace host to db in the future
    return psycopg.connect(f"host={host} port={port} user=noisitor password={password}")
