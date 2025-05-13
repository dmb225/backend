import json
import os
import signal
import subprocess
import time
from pathlib import Path
from typing import Optional

import click
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

APPLICATION_CONFIG_PATH = "config"
DOCKER_PATH = "docker"


def setenv(variable: str, default: str) -> None:
    os.environ[variable] = os.getenv(variable, default)


def read_json_configuration(config: str) -> dict[str, str]:
    with open(Path(APPLICATION_CONFIG_PATH) / f"{config}.json") as f:
        config_data = json.load(f)

    config_data = dict((i["name"], i["value"]) for i in config_data)

    return config_data


def configure_app(config: dict[str, str]) -> None:
    configuration = read_json_configuration(config)

    for key, value in configuration.items():
        setenv(key, value)
        print(f"Set environment variable: {key} = {value}")


def docker_compose_cmdline(commands_string: Optional[str] = None) -> list[str]:
    config = os.getenv("APPLICATION_CONFIG")
    configure_app(config)

    compose_file = Path(DOCKER_PATH) / f"{config}.yml"

    if not compose_file.is_file():
        raise ValueError(f"The file {compose_file} does not exist")

    command_line = [
        "docker",
        "compose",
        "-p",
        config,
        "-f",
        str(compose_file),
    ]

    if commands_string:
        command_line.extend(commands_string.split(" "))

    return command_line


def run_sql(statements):
    conn = psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("POSTGRES_HOSTNAME"),
        port=os.getenv("POSTGRES_PORT"),
    )

    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()
    for statement in statements:
        cursor.execute(statement)

    cursor.close()
    conn.close()


def wait_for_logs(cmdline, message):
    logs = subprocess.check_output(cmdline)
    while message not in logs.decode("utf-8"):
        time.sleep(1)
        logs = subprocess.check_output(cmdline)


@click.group()
def cli():
    pass


@cli.command()
@click.argument("args", nargs=-1)
def test(args):
    setenv("APPLICATION_CONFIG", "testing")
    configure_app(os.getenv("APPLICATION_CONFIG"))

    cmdline = docker_compose_cmdline("up -d")
    subprocess.call(cmdline)

    cmdline = docker_compose_cmdline("logs postgres")
    wait_for_logs(cmdline, "ready to accept connections")

    run_sql([f"CREATE DATABASE {os.getenv('APPLICATION_DB')}"])

    cmdline = [
        "pytest",
        "-svv",
        "--cov=src",
        "--cov-report=term-missing",
    ]
    cmdline.extend(args)
    subprocess.call(cmdline)

    cmdline = docker_compose_cmdline("down")
    subprocess.call(cmdline)


@cli.command(context_settings={"ignore_unknown_options": True})
@click.argument("subcommand", nargs=-1, type=click.Path())
def compose(subcommand):
    setenv("APPLICATION_CONFIG", "production")
    configure_app(os.getenv("APPLICATION_CONFIG"))

    cmdline = docker_compose_cmdline() + list(subcommand)
    print(f"Running: {' '.join(cmdline)}")
    try:
        p = subprocess.Popen(cmdline)
        p.wait()
    except KeyboardInterrupt:
        p.send_signal(signal.SIGINT)
        p.wait()


@cli.command()
def init_postgres():
    setenv("APPLICATION_CONFIG", "production")
    configure_app(os.getenv("APPLICATION_CONFIG"))

    try:
        run_sql([f"CREATE DATABASE {os.getenv('APPLICATION_DB')}"])
    except psycopg2.errors.DuplicateDatabase:
        print(
            (
                f"The database {os.getenv('APPLICATION_DB')} already",
                "exists and will not be recreated",
            )
        )


if __name__ == "__main__":
    cli()
