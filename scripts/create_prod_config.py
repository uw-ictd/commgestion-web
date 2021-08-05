#! /usr/bin/env python3

"""Create a production ready commgestion configuration file from scratch
"""

import getpass
import os
import secrets
import shutil
import toml


def create_config_tree():
    key_answer = input("Generate a random secret key? [y]/n:")
    if key_answer.lower() == "n":
        secret_key = input("Input the desired secret key now:")
    else:
        secret_key_choices = "abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)"
        secret_key = [secrets.choice(secret_key_choices) for _ in range(50)]
        secret_key = "".join(secret_key)

    allowed_hosts = []
    while True:
        host_answer = input("server hostname [localhost]:")
        if host_answer == "":
            host_answer = "localhost"
        allowed_hosts.append(host_answer)
        another = input("Add another hostname? y/[n]:")
        if another.lower() == "y":
            continue
        else:
            break

    database_host = input('postgres host ["localhost"]:')
    if database_host == "":
        database_host = "localhost"

    database_port = input("postgres port [5432]:")
    if database_port == "":
        database_port = 5432

    database_name = input("postgres database name [commgestionProd]:")
    if database_name == "":
        database_name = "commgestionProd"

    database_username = input("postgres user [commgestion]:")
    if database_username == "":
        database_username = "commgestion"

    print("Warning: db password will be written unencrypted to local disk")
    database_password = getpass.getpass("postgres password:")

    config = {
        "commgestion": {
            "debug": False,
            "secret_key": secret_key,
            "allowed_hosts": allowed_hosts,
            "db": {
                "kind": "postgres",
                "database": database_name,
                "username": database_username,
                "password": database_password,
                "host": database_host,
                "port": database_port,
            },
        }
    }

    return config


if __name__ == "__main__":
    generated_config = create_config_tree()
    with open("config-prod.toml", mode="w+") as f:
        toml.dump(generated_config, f)

    try:
        os.makedirs(os.path.join("/", "etc", "commgestion"))
    except PermissionError as e:
        print("Insufficient permissions to create configuration directory")
        raise e
    except FileExistsError:
        # The directory already exists.
        pass

    if os.path.exists(os.path.join("/", "etc", "commgestion", "config.toml")):
        overwrite = input("overwrite existing config? y/[n]")
        if overwrite.lower() != "y":
            print("Will not overwrite existing configuration!")
            print(
                "The generated file has been left in the local directory at "
                '"config-prod.toml"'
            )
            raise FileExistsError("existing configuration")

    try:
        shutil.move(
            "config-prod.toml", os.path.join("/", "etc", "commgestion", "config.toml")
        )
    except PermissionError as e:
        print("Insufficient permissions to move the config file!")
        print(
            "The generatedfile has been left in the local directory at "
            '"config-prod.toml"'
        )
        print(
            "Please move this file to /etc/commgestion/config.toml, "
            "perhaps with sudo :D"
        )
        raise e

    print("configuration generated and deployed to " "/etc/commgestion/config.toml")
