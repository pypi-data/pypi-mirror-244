#!/usr/bin/env python3
import getpass
import json
import os

import warnings
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import click
import requests

from dataset_sh.utils.files import upload_to_url
from .core import DatasetFileMeta
from .dep import DatasetDependencies, locate_dep_file, get_dataset_url_for_remote_host, DatasetDependencyItem
from .io import DatasetStorageManager, read_file, import_remote as io_import_remote
from .models import DatasetClientProfileConfig
from .typing.codegen import CodeGenerator
from .utils.misc import parse_dataset_name


def fetch_project_definition_or_fail(project_folder):
    project_file = None
    if project_folder is None:
        project_file = locate_dep_file(os.getcwd())
    else:
        fp = os.path.join(project_folder, 'dataset.list')
        if os.path.exists(fp):
            project_file = fp

    if project_file is None:
        click.echo('Cannot find project file, use init command to create an empty one.')
        click.echo('')
        raise click.Abort()

    project_def = DatasetDependencies.read_from_file(project_file)
    return project_file, project_def


@dataclass
class AppCtx:
    base: Optional[str] = None


@click.group(name='dataset.sh')
@click.option('--base', '-b', envvar='DATASET_SH_STORAGE_BASE', help='location of base storage folder.',
              type=click.Path())
@click.pass_context
def cli(ctx, base):
    """Simple CLI tool with subcommands"""
    ctx.obj = DatasetStorageManager(store_base=base)


@click.command(name='print')
@click.argument('name')
@click.argument('action', type=click.Choice(['list-collections', 'readme', 'code', 'sample']))
@click.option('--collection', '-c', help='which collection')
@click.pass_obj
def print_info(manager: DatasetStorageManager, name, action, collection):
    """
    print dataset information
    """
    username, dataset_name = parse_dataset_name(name)

    if action in [
        'code',
        'sample',
    ] and (collection is None or collection == ''):
        click.echo('You must provide a collection using --collection/-c')
        raise click.Abort()

    if action == 'list-collections':
        meta = manager.get_dataset_meta(username, dataset_name)
        meta = DatasetFileMeta(**meta)

        click.echo(f'Total collections: {len(meta.collections)}')
        for coll in meta.collections:
            click.echo(coll.name)

    elif action == 'readme':
        readme = manager.get_dataset_readme(username, dataset_name)
        click.echo(readme)

    elif action == 'code':
        code = manager.get_usage_code(username, dataset_name, collection_name=collection)
        click.echo(code)

        meta = manager.get_dataset_meta(username, dataset_name)
        meta = DatasetFileMeta(**meta)
        coll = meta.find_collection(collection)

        if coll is not None:
            loader_code = CodeGenerator.generate_loader_code(
                username,
                dataset_name,
                collection,
                coll.data_schema.entry_point)
            click.echo('\n\n')
            click.echo(loader_code)

    elif action == 'sample':
        sample = manager.get_sample(username, dataset_name, collection)
        click.echo(json.dumps(sample, indent=2))


@click.command(name='inspect-file')
@click.argument('filepath', type=click.Path())
@click.argument('action', type=click.Choice(['list-collections', 'code', 'sample']))
@click.option('--collection', '-c', help='which collection.')
@click.pass_obj
def inspect_file(manager: DatasetStorageManager, filepath, action, collection):
    """
    parse dataset file and print out information
    """

    if action in [
        'code',
        'sample',
    ] and (collection is None or collection == ''):
        click.echo('You must provide a collection using --collection/-c')
        raise click.Abort()

    with read_file(filepath) as reader:
        if action == 'list-collections':
            collections = reader.collections()
            click.echo(f'Total collections: {len(collections)}')
            for coll in collections:
                click.echo(coll)

        elif action == 'code':
            coll = reader.collection(collection)
            code = coll.code_usage()
            schema = coll.config.data_schema
            loader_code = CodeGenerator.generate_file_loader_code(filepath, collection, schema.entry_point)
            click.echo(code)
            click.echo('\n\n')
            click.echo(loader_code)

        elif action == 'sample':
            sample = reader.collection(collection).top()
            click.echo(json.dumps(sample, indent=2))


@click.command(name='remove-imported')
@click.argument('name')
@click.option('--force', '-f', default=False, help='Force remove dataset without confirmation.', is_flag=True)
@click.pass_obj
def remove(manager: DatasetStorageManager, name, force):
    """remove a managed dataset"""
    username, dataset_name = parse_dataset_name(name)
    if not force:
        confirmation = click.prompt(f'Are you sure you want to remove dataset {name}? (y/N): ')
        if confirmation.lower() == 'y':
            manager.delete_dataset(username, dataset_name)
    else:
        manager.delete_dataset(username, dataset_name)


@click.command(name='list')
@click.option('--store', '-s', help='select dataset store space to list.')
@click.pass_obj
def list_datasets(manager: DatasetStorageManager, store):
    """list datasets"""
    items = []
    if store:
        items = manager.list_datasets_in_store(store).items
    else:
        items = manager.list_datasets().items

    click.echo(f'\nFound {len(items)} datasets:\n')
    items = sorted(items, key=lambda x: f'{x.datastore} / {x.dataset}')
    for item in items:
        click.echo(f'  {item.datastore}/{item.dataset}')
    click.echo('')


@click.command(name='import')
@click.argument('name')
@click.option('--url', '-u', help='url of the dataset file to import')
@click.option('--file', '-f', help='local file path of the dataset file to import', type=click.Path())
@click.option('--host', '-h', help='host server url', default='https://export.dataset.sh/dataset')
@click.pass_obj
def import_(manager, name, url, file, host):
    """import dataset from url or file"""
    if url is not None and file is not None:
        click.echo('Usage: import [NAME] -u [url]')
        click.echo('Usage: import [NAME] -f [file-path]')
        raise click.Abort()

    username, dataset_name = parse_dataset_name(name)

    if url is not None:
        click.echo(f'importing remote file from {url}')
        manager.import_url(url, username, dataset_name)
    elif file is not None:
        click.echo(f'importing local file from {file}')
        manager.import_file(file, username, dataset_name)
    else:
        remote_url = get_dataset_url_for_remote_host(host, name)
        username, dataset = parse_dataset_name(name)
        manager.import_url(remote_url, username, dataset)


@click.command(name='import-remote')
@click.argument('name')
@click.option('--target', '-t', help='local name for the imported dataset', default=None)
@click.pass_obj
def import_remote(manager, name, target):
    """Edit readme of a dataset"""
    if target is None:
        target = name
    io_import_remote(name, rename=target, store_base=manager.base)


@click.command(name='init')
@click.option('--project', '-p', 'project_folder', help='project folder', default=None)
@click.pass_obj
def init_project(manager, project_folder):
    """create an empty dataset.list file at current folder"""
    project_def = DatasetDependencies()
    if project_folder is None:
        project_folder = './'
    fp = os.path.join(project_folder, 'dataset.list')
    if os.path.exists(fp):
        click.echo('dataset.list already exists.')
        return
    else:
        project_def.write_to_file(fp)


@click.command(name='install')
@click.option('--dataset', '-d', help='add a dataset', default=None)
@click.option('--rename', '-r', help='rename this dataset locally', default=None)
@click.option('--host', '-h', help='host', default='https://export.dataset.sh/dataset')
@click.option('--project', '-p', 'project_folder', help='project folder', default=None)
@click.pass_obj
def install_project(manager, dataset, rename, host, project_folder):
    """import dataset from a dataset project file, or add a dataset to a dataset project file"""
    project_file, project_def = fetch_project_definition_or_fail(project_folder)

    for d in project_def.datasets:
        target_name = d.name if d.rename is None else d.rename
        username, dataset_name = parse_dataset_name(target_name)
        url = get_dataset_url_for_remote_host(host, d.name)
        manager.import_url(url, username, dataset_name, exist_ok=True)

    if dataset is not None:
        target_name = rename if rename is not None else dataset

        if project_def.has(target_name):
            click.echo('Item already exists.')
            click.echo('')
            raise click.Abort()

        remote_url = get_dataset_url_for_remote_host(host, dataset)
        username, dataset_name = parse_dataset_name(target_name)
        if rename is not None:
            username, dataset_name = parse_dataset_name(rename)
        manager.import_url(remote_url, username, dataset_name, exist_ok=True)
        project_def.add_dataset(DatasetDependencyItem(name=dataset, rename=rename))
        project_def.write_to_file(project_file)


@click.command(name='remove')
@click.argument('name')
@click.option('--project', '-p', 'project_folder', help='project folder', default=None)
@click.pass_obj
def remove_from_project(manager: DatasetStorageManager, name, project_folder):
    """remove dataset from project"""
    project_file, project_def = fetch_project_definition_or_fail(project_folder)
    project_def.remove(name)
    project_def.write_to_file(project_file)


@click.command(name='upload')
@click.argument('target_name')
@click.option('--name', '-n', 'name', help='name of local dataset to upload.', default=None)
@click.option('--file', '-f', 'file', help='path to local dataset to upload.', default=None)
@click.option('--host', '-h', 'host', help='host address.', default=None)
@click.option('--profile', '-p', 'profile_name', help='host address.', default=None)
@click.pass_obj
def upload(manager: DatasetStorageManager, target_name, name, file, host, profile_name):
    """upload dataset to server"""

    file_path = None

    if file:
        file_path = file
    elif name:
        username, dataset_name = parse_dataset_name(name)
        file_path = manager.get_dataset_file_path(username, dataset_name)
    else:
        username, dataset_name = parse_dataset_name(target_name)
        file_path = manager.get_dataset_file_path(username, dataset_name)

    if not os.path.exists(file_path):
        click.echo(f'{file_path} do not exists')
        click.echo('')
        raise click.Abort()

    if not host.endswith('/'):
        host = host + '/'
    upload_url = f'{host}api/dataset'

    # create params
    username, dataset_name = parse_dataset_name(target_name)

    params = {
        "userName": username,
        "datasetName": dataset_name
    }

    # gather headers
    profiles = DatasetClientProfileConfig.load_profiles()
    profile = profiles.find_matching_profile(host, profile_name)
    headers = {}
    if profile and profile.key:
        headers = {"X-DATASET-SH-ACCESS-KEY": profile.key}
    else:
        click.echo('Cannot find access key for this host. \n')
        raise click.Abort()

    upload_to_url(upload_url, file_path, headers, params, target_name)


@click.command(name='add-access-key')
@click.option('--host', '-h', 'host', help='host address.', default=None)
@click.option('--name', '-n', 'profile_name', help='profile name.', default=None)
@click.pass_obj
def add_key(manager: DatasetStorageManager, host, profile_name):
    cfg = DatasetClientProfileConfig.load_profiles()
    if host is None:
        host = input('Host: ').strip()

    if cfg.find_matching_profile(url=host):
        click.echo("")
        click.echo('Find existing profile with the same host.')
        click.echo('You can use profile name to select which key to use in the future.')
        click.echo("")

    if profile_name is None:
        profile_name = input('Profile Name (Optional): ').strip()
        if profile_name == '':
            profile_name = None

    key = getpass.getpass('Enter your access key (Your input will be hidden): ').strip()

    if key == '' or key is None:
        click.echo('Key is empty. \n')
        raise click.Abort()

    cfg.add_profile(host, key, name=profile_name)
    cfg.save()

    click.echo(f'New profile saved in {DatasetClientProfileConfig.get_profile_file_path()}')


cli.add_command(print_info)
cli.add_command(remove)
cli.add_command(list_datasets)
cli.add_command(inspect_file)
cli.add_command(import_)
cli.add_command(import_remote)

cli.add_command(init_project)
cli.add_command(install_project)
cli.add_command(remove_from_project)
cli.add_command(upload)

cli.add_command(add_key)

if __name__ == '__main__':  # pragma: no cover
    cli()
