import os
from subprocess import Popen
import logging
from typing import Optional
import site

import requests
import click
import uvicorn

from ellipsis.ellipsis_api_client import EllipsisApiClient
from ellipsis.src.listener.cloud_dev_env_listener import CloudDevEnvListener
from ellipsis.src.models.workspaces.constants import HEALTH_CHECK_URL_ROUTE, LISTENER_PORT


CLI_VERSION = '0.2.1'

@click.group()
def cli():
    pass

@cli.command()
def version():
    click.echo(f"Version {CLI_VERSION}")

@cli.command()
def ping():
    api_client = EllipsisApiClient(os.environ.get('ELLIPSIS_API_URL', None))
    click.echo(f'Pinging {api_client.base_url}...')
    click.echo("Success!")

@click.group()
def listener():
    pass

@listener.command()
@click.argument('repo_dir')
def start(repo_dir: str):
    # Get all the required env vars
    codespace_name = _expect_env_var_to_exist('CODESPACE_NAME')
    github_token = _expect_env_var_to_exist('GITHUB_TOKEN')
    github_user = _expect_env_var_to_exist('GITHUB_USER')
    github_repository = _expect_env_var_to_exist('GITHUB_REPOSITORY')

    api_client = EllipsisApiClient(os.environ.get('ELLIPSIS_API_URL', None))
    repo_name_split = github_repository.split('/')
    assert len(repo_name_split) == 2, f'Invalid repository name: {github_repository}'
    api_client.register_codespace(
        codespace_name,
        repo_name_split[0],
        repo_name_split[1],
        github_token,
        github_user
    )
    try:
        response = requests.get(f"http://localhost:{LISTENER_PORT}{HEALTH_CHECK_URL_ROUTE}")
        if response.status_code == 200:
            click.echo("Listener already running.")
            return
    except requests.exceptions.ConnectionError:
        # Listener not running, so we can start it
        pass
    module_path = os.path.dirname(__file__)
    listener_file_path = os.path.join(module_path, '_listener.py')
    background_process = Popen(['python3', listener_file_path, repo_dir])
    click.echo(f"Starting listener in background process with PID {background_process.pid}...")


@listener.command()
def stop():
    raise NotImplementedError(f'Not implemented for some archietctures.')
    # try:
    #     response = requests.get(f"http://localhost:{LISTENER_PORT}{HEALTH_CHECK_URL_ROUTE}")
    #     click.echo(response.json())
    #     if response.status_code != 200:
    #         click.echo("Listener not running, nothing to stop.")
    #         return
    # except requests.exceptions.ConnectionError:
    #     click.echo("Listener not running, nothing to stop.")
    #     return
    # response_json = response.json()
    # pid = response_json['pid']
    # Popen(['kill', str(pid)])
    # click.echo(f"Killed listener with PID {pid}.")

cli.add_command(ping)
cli.add_command(version)
cli.add_command(listener)


def _expect_env_var_to_exist(env_var_name: str):
    env_var_value = os.environ.get(env_var_name, None)
    if env_var_value is None:
        raise ValueError(f"Environment variable {env_var_name} not set.")
    return env_var_value

if __name__ == '__main__':
    cli()
