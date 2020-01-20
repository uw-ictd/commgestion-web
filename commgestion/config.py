# To ensure that the postgres Database connections and migrations work, it is necessary to install
# 1. psycopg2 (managed by pipenv in this project)
#    - In case you run into problems with openssl versions or clang causing errors with -lssl on mac,
#      first and foremost validate the presence of libssl with `locate libssl` followed by linking using:
#      `export LIBRARY_PATH=$LIBRARY_PATH:/usr/local/opt/openssl/lib/`

DATABASE_CONFIG = {
    'NAME': 'commgestionDev',
    'USER': 'commgestion',
    'PASSWORD': '',
    'HOST': '0.0.0.0',
    'PORT': '5432',
}