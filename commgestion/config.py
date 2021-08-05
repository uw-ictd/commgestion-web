import logging
import tomlkit

# To ensure that the postgres Database connections and migrations work,
# it is necessary to install
#
# 1. psycopg2 (managed by pipenv in this project) - In case you run into
# problems with openssl versions or clang causing errors with -lssl on mac,
# first and foremost validate the presence of libssl with `locate libssl`
# followed by linking using: `export
# LIBRARY_PATH=$LIBRARY_PATH:/usr/local/opt/openssl/lib/`

log = logging.getLogger(__name__)


def parse_from_file(filepath):
    """Load a TOML formatted configuration file and parse commgestion parameters"""
    config = {}
    with open(filepath) as f:
        raw_config = tomlkit.parse(f.read())

    try:
        config["debug"] = bool(raw_config["commgestion"]["debug"])
    except KeyError:
        log.info('"debug" config not defined, defaulting to false')
        config["debug"] = False

    try:
        config["secret_key"] = str(raw_config["commgestion"]["secret_key"])
    except (KeyError, TypeError) as e:
        log.error('"secret_key" is required and must be a string!')
        raise e

    try:
        config["allowed_hosts"] = raw_config["commgestion"]["allowed_hosts"]
    except KeyError:
        log.info("allowed_hosts")

    config["db"] = _parse_database_config(raw_config["commgestion"]["db"])

    return config


def _parse_database_config(raw_db_config):
    """Parse a database configuration appropriate for django

    For more info see https://docs.djangoproject.com/en/3.0/ref/settings
    /#databases
    """
    try:
        kind = raw_db_config["kind"]
    except KeyError as e:
        log.error('The database "kind" must be specified')
        raise e

    if kind == "sqlite3":
        try:
            path = raw_db_config["path"]
        except KeyError:
            log.info('sqlite db "path" is not specified, using default')
            path = "db.sqlite3"

        db_config = {
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": "./db.sqlite3",
            }
        }

        return db_config
    elif kind == "postgres":
        try:
            database = raw_db_config["database"]
            username = raw_db_config["username"]
            password = raw_db_config["password"]
            host = raw_db_config["host"]
            port = raw_db_config["port"]
        except KeyError as e:
            log.error("Postgres db configuration parameter is missing!")
            raise e

        db_config = {
            "default": {
                "ENGINE": "django.db.backends.postgresql",
                "NAME": database,
                "USER": username,
                "PASSWORD": password,
                "HOST": host,
                "PORT": port,
            }
        }

        return db_config

    raise NotImplementedError("Database kind {} is not supported".format(kind))
