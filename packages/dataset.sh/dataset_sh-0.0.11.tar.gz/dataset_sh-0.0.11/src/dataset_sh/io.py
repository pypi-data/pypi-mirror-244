import json
import os
import shutil
import tempfile
import time
import uuid
import warnings
import zipfile
from typing import Optional, Type, TypeVar, List

from pydantic import BaseModel, ValidationError

from .config import get_storage_base_folder
from .dep import get_dataset_url_for_remote_host
from .models import DatasetInfoSnippet, NamespaceList, DatasetListingResults, DatasetHomeFolder, \
    SourceInfo, DatasetFileInternalPath, DatasetClientProfileConfig
from .typing.codegen import CodeGenerator
from .typing.schema_builder import SchemaBuilder
from .utils.files import download_url
from .utils.misc import readfile_or_default, is_name_legit, parse_dataset_name, read_jsonl, try_parse_error, \
    id_function
from .core import CollectionConfig, DatasetFileMeta
from .utils.sample import reservoir_sampling

DataModel = TypeVar('DataModel', bound=BaseModel)


class DatasetFile:

    def __init__(self):
        raise ValueError('Please use DatasetFile.open(filename, mode)')

    @staticmethod
    def open(fp: str, mode: str = 'r'):
        """
        Open a dataset file
        :param fp: path to the file
        :param mode: r for read and w for write.
        :return:
        """
        if mode == 'r':
            return DatasetFileReader(fp)
        elif mode == 'w':
            return DatasetFileWriter(fp)
        else:
            raise ValueError('mode must be one of "r" or "w"')

    @staticmethod
    def binary_file_path(fn: str):
        return os.path.join(DatasetFileInternalPath.BINARY_FOLDER, fn)


class DatasetFileWriter:
    def __init__(self, file_path: str, compression=zipfile.ZIP_LZMA, compresslevel=9):
        """
        Write to a dataset file, this object can also be used as a context manager.

        This object need to be closed.

        :param file_path: location of the dataset file to write.
        :param compression: compress mode for zip file.
        :param compresslevel: note that the default compression algorithm ZIP_LZMA do not use this value.

        """
        self.zip_file = zipfile.ZipFile(file_path, 'w', compression=compression, compresslevel=compresslevel)
        self.meta = DatasetFileMeta()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        """
        close the writer.
        :return:
        """
        self.meta.createdAt = int(time.time())
        with self.zip_file.open(DatasetFileInternalPath.META_FILE_NAME, 'w') as out:
            out.write(self.meta.model_dump_json().encode('utf-8'))
        self.zip_file.close()

    def add_collection(
            self,
            collection_name: str,
            data: List,
            model: Optional[Type[DataModel]] = None,
            tqdm=id_function,
    ):
        """
        add a data collection to this dataset.
        :param collection_name: name of the collection to add.
        :param data: list of objects that extends pydantic BaseModel.
        :param model: the pydantic model class.
        :param tqdm: Optional tqdm progress bar.
        :return:
        """
        for coll in self.meta.collections:
            if coll.name == collection_name:
                raise ValueError(f'collection {collection_name} already exists')

        if model is None:
            if isinstance(data[0], BaseModel):
                warnings.warn(f'model class is not provided, using {data[0].__class__.__name__} as model')
                model = data[0].__class__
            else:
                raise ValueError('Input data must be pydantic model')

        dataset_schema = SchemaBuilder.build(model)

        new_coll = CollectionConfig(
            name=collection_name,
            data_schema=dataset_schema,
        )

        self.meta.collections.append(new_coll)
        target_fp = os.path.join(
            DatasetFileInternalPath.COLLECTION_FOLDER,
            collection_name,
            DatasetFileInternalPath.DATA_FILE
        )
        with self.zip_file.open(target_fp, 'w') as out:
            for item in tqdm(data):
                out.write(item.model_dump_json(round_trip=True).encode('utf-8'))
                out.write("\n".encode('utf-8'))

    def add_binary_file(self, fn: str, content: bytes):
        """
        Add a binary file to the dataset
        :param fn: name of the binary file.
        :param content: content in bytes.
        :return:
        """
        binary_file_path = DatasetFile.binary_file_path(fn)
        with self.zip_file.open(binary_file_path, 'w') as out:
            out.write(content)


class DatasetFileReader:
    def __init__(self, file_path):
        """
        Read a dataset, this object can be used as a context manager.

        This object must be closed.

        :param file_path:
        """
        self.zip_file = zipfile.ZipFile(file_path, 'r')

        with self.zip_file.open(DatasetFileInternalPath.META_FILE_NAME, 'r') as fd:
            self.meta = DatasetFileMeta(**json.load(fd))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        self.zip_file.close()

    def binary_files(self):
        """
        Open a binary file for read.
        :return: a file descriptor for the binary file to read.
        """
        prefix = DatasetFileInternalPath.BINARY_FOLDER + '/'
        for name in self.zip_file.namelist():
            if name.startswith(prefix):
                yield name[len(prefix):]

    def open_binary_file(self, filename):
        """
        Open a binary file for read.
        :param filename: name of the binary file.
        :return: a file descriptor for the binary file to read.
        """
        return self.zip_file.open(
            DatasetFile.binary_file_path(filename),
            'r'
        )

    def collection(self, collection_name, model=None):
        """
        Open a collection.
        :param collection_name: name of a collection
        :param model: an optional pydantic model class to hold the data.
        :return: a CollectionReader object for the given collection name.
        """
        cfg = [c for c in self.meta.collections if c.name == collection_name]
        if len(cfg) == 0:
            raise ValueError(f"Collection {collection_name} do not exist")
        else:
            cfg = cfg[0]
        return CollectionReader(self.zip_file, collection_name, cfg, model=model)

    def coll(self, collection_name, model=None):
        return self.collection(collection_name, model=model)

    def collections(self):
        """
        List all collection names
        :return: list of collection names.
        """
        return [c.name for c in self.meta.collections]

    def __getitem__(self, item):
        return self.collection(item)


class CollectionReader(object):
    def __init__(self, zip_file, collection_name, config: CollectionConfig, model=None):
        """
        Collection Reader
        :param zip_file:
        :param collection_name:
        :param config:
        :param model:
        """
        self.zip_file = zip_file
        self.collection_name = collection_name
        self.config = config
        self.model = model

    def code_usage(self):
        generator = CodeGenerator()
        code = generator.generate_all(self.config.data_schema)
        return code

    def top(self, n=10):
        ret = []
        for i, row in enumerate(self):
            if i >= n:
                break
            ret.append(row)
        return ret

    def random_sample(self, n=10):
        return reservoir_sampling(self, n)

    def __iter__(self):
        """
        Iterate through the collection.
        :return:
        """
        entry = os.path.join(
            DatasetFileInternalPath.COLLECTION_FOLDER,
            self.collection_name,
            DatasetFileInternalPath.DATA_FILE
        )
        with self.zip_file.open(entry, 'r') as fd:
            for line in fd:
                line = line.strip()
                if len(line) > 0:
                    item = json.loads(line)
                    if self.model is None:
                        yield item
                    else:
                        yield self.model(**item)

    def to_list(self):
        """
        Read the collection as list instead of iterator
        :return:
        """
        return list(self)


class DatasetStorageManager:
    def __init__(self, store_base=None):
        if store_base is None or store_base == '':
            store_base = get_storage_base_folder()
        self.base = store_base
        self.profiles = DatasetClientProfileConfig.load_profiles().profiles

    def list_dataset_stores(self) -> NamespaceList:
        base_dir = self.base
        stores = []

        if os.path.exists(base_dir):

            for store_name in os.listdir(base_dir):
                store_dir = os.path.join(base_dir, store_name)

                if os.path.isdir(store_dir) and is_name_legit(store_name):
                    stores.append(store_name)

        return NamespaceList(stores=stores)

    def list_datasets(self) -> DatasetListingResults:
        base_dir = self.base
        datasets = []

        if os.path.exists(base_dir):
            for store_name in os.listdir(base_dir):
                store_dir = os.path.join(base_dir, store_name)

                if os.path.isdir(store_dir):
                    for dataset_name in os.listdir(store_dir):
                        dataset_dir = os.path.join(store_dir, dataset_name)
                        dataset_home_folder = DatasetHomeFolder(dataset_dir)
                        if dataset_home_folder.marker_exist():
                            readme = readfile_or_default(dataset_home_folder.readme())
                            datasets.append(DatasetInfoSnippet(
                                datastore=store_name,
                                dataset=dataset_name,
                                readme=readme
                            ))
        return DatasetListingResults(items=datasets)

    def list_datasets_in_store(self, store_name) -> DatasetListingResults:
        base_dir = self.base
        datasets = []

        store_dir = os.path.join(base_dir, store_name)
        if os.path.isdir(store_dir):
            for dataset_name in os.listdir(store_dir):
                dataset_dir = os.path.join(store_dir, dataset_name)
                dataset_home_folder = DatasetHomeFolder(dataset_dir)
                if dataset_home_folder.marker_exist():
                    readme = readfile_or_default(dataset_home_folder.readme())
                    datasets.append(DatasetInfoSnippet(
                        datastore=store_name,
                        dataset=dataset_name,
                        readme=readme
                    ))
        return DatasetListingResults(items=datasets)

    def get_dataset_dir(self, username, dataset_name):
        store_dir = os.path.join(self.base, username, dataset_name)
        return DatasetHomeFolder(store_dir)

    def get_dataset_meta(self, username, dataset_name):
        dataset_home_folder = self.get_dataset_dir(username, dataset_name)
        return json.loads(readfile_or_default(dataset_home_folder.meta()))

    def get_dataset_source_info(self, username, dataset_name) -> Optional[SourceInfo]:
        dataset_home_folder = self.get_dataset_dir(username, dataset_name)
        source_json = readfile_or_default(dataset_home_folder.remote_source(), None)
        if source_json is not None:
            return SourceInfo(**json.loads(source_json))
        return None

    def get_dataset_file_path(self, username, dataset_name):
        dataset_home_folder = self.get_dataset_dir(username, dataset_name)
        return dataset_home_folder.datafile()

    def get_dataset_readme(self, username, dataset_name):
        dataset_home_folder = self.get_dataset_dir(username, dataset_name)
        return readfile_or_default(dataset_home_folder.readme())

    def update_dataset_readme(self, username, dataset_name, content):
        dataset_home_folder = self.get_dataset_dir(username, dataset_name)
        with open(dataset_home_folder.readme(), 'w') as out:
            out.write(content)

    def get_sample(self, username, dataset_name, collection):
        dataset_home_folder = self.get_dataset_dir(username, dataset_name)
        if os.path.isfile(dataset_home_folder.sample_file(collection)):
            with open(dataset_home_folder.sample_file(collection)) as fd:
                return list(read_jsonl(fd))
        return []

    def get_usage_code(self, username, dataset_name, collection_name):
        meta = self.get_dataset_meta(username, dataset_name)
        meta = DatasetFileMeta(**meta)
        cs = [c for c in meta.collections if c.name == collection_name]
        if len(cs) > 0:
            cg = CodeGenerator()
            return cg.generate_all(cs[0].data_schema)
        else:
            return ''

    def dataset_exist(self, username, dataset_name):
        dataset_home_folder = self.get_dataset_dir(username, dataset_name)
        return dataset_home_folder.marker_exist()

    def delete_dataset(self, username, dataset_name):
        dataset_home_folder = self.get_dataset_dir(username, dataset_name)
        shutil.rmtree(dataset_home_folder.base)

    def import_file(self, file, username, dataset_name, source_url=None, exist_ok=True, remove_source=False):
        if self.dataset_exist(username, dataset_name):
            if exist_ok:
                print(f'dataset {username}/{dataset_name} already exists')
                return
            else:
                raise ValueError(f'dataset {username}/{dataset_name} already exists')

        dataset_folder = self.get_dataset_dir(username, dataset_name)
        os.makedirs(
            dataset_folder.base, exist_ok=True
        )

        if remove_source:
            shutil.move(file, dataset_folder.datafile())
        else:
            shutil.copy2(file, dataset_folder.datafile())

        self.extract_sample_and_code_usage(dataset_folder.datafile(), dataset_folder)

        if source_url is not None:
            with open(dataset_folder.remote_source(), 'w') as out:
                info = SourceInfo(url=source_url)
                json.dump(info.model_dump(mode='json'), out)

        with open(dataset_folder.marker(), 'w') as out:
            out.write('1')

    def find_matching_profile(self, url, profile_name=None):
        if profile_name is not None:
            for p in self.profiles:
                if p.name == profile_name:
                    return p
        else:
            for p in self.profiles:
                if url.startswith(p.host):
                    return p

    def import_url(self, url, username, dataset_name, profile_name=None, exist_ok=True):
        if self.dataset_exist(username, dataset_name):
            if exist_ok:
                print(f'dataset {username}/{dataset_name} already exists')
                return
            else:
                raise ValueError(f'dataset {username}/{dataset_name} already exists')

        headers = None
        p = self.find_matching_profile(url, profile_name=profile_name)

        if p and p.key:
            headers = {"X-DATASET-SH-ACCESS-KEY": p.key}

        with tempfile.TemporaryDirectory() as temp_dir:
            file_name = str(uuid.uuid4())
            temp_file_path = os.path.join(temp_dir, file_name)
            download_url(url, temp_file_path, headers)
            import shutil
            shutil.copyfile(temp_file_path, '/tmp/debug')

            self.import_file(temp_file_path, username, dataset_name, source_url=url, remove_source=True)

        return self.get_dataset_file_path(username, dataset_name)

    @staticmethod
    def extract_sample_and_code_usage(data_file, dataset_folder):
        with read_file(data_file) as reader:
            meta_file_dest = dataset_folder.meta()
            with reader.zip_file.open(DatasetFileInternalPath.META_FILE_NAME, 'r') as fd:
                with open(meta_file_dest, 'wb') as out:
                    out.write(fd.read())

            for coll_name in reader.collections():
                coll = reader.collection(coll_name)
                with open(dataset_folder.sample_file(coll_name), 'w') as out:
                    samples = coll.top(n=10)
                    for item in samples:
                        out.write(f'{json.dumps(item)}\n')
                with open(dataset_folder.code_example(coll_name), 'w') as out:
                    code = coll.code_usage()
                    out.write(code)


# Standard IO operations

def create(fp: str, compression=zipfile.ZIP_LZMA, compresslevel=9) -> 'DatasetFileWriter':
    """
    Create a dataset file to write
    :param fp: path to the file
    :param compression: compress mode for zip file.
    :param compresslevel: note that the default compression algorithm ZIP_LZMA do not use this value.
    :return:
    """
    return DatasetFileWriter(fp, compression=compression, compresslevel=compresslevel)


def read_file(fp: str) -> 'DatasetFileReader':
    """
    Read a dataset file
    :param fp: path to the file
    :return:
    """
    return DatasetFileReader(fp)


def read(name: str, store_base: Optional[str] = None) -> 'DatasetFileReader':
    """
    Read a managed dataset file by name.
    :param name: name of the dataset file to locate
    :param store_base: where is the base folder or app
    :return:
    """
    manager = DatasetStorageManager(store_base)
    username, dataset_name = parse_dataset_name(name)
    located = manager.get_dataset_file_path(username, dataset_name)
    if os.path.exists(located):
        return DatasetFileReader(located)
    else:
        raise FileNotFoundError()


def import_file(name, file, store_base=None, exist_ok=True):
    manager = DatasetStorageManager(store_base=store_base)
    username, dataset = parse_dataset_name(name)
    manager.import_file(file, username, dataset, exist_ok=exist_ok)


def import_url(name, url, store_base=None, exist_ok=True, profile=None):
    manager = DatasetStorageManager(store_base=store_base)
    username, dataset = parse_dataset_name(name)
    manager.import_url(url, username, dataset, exist_ok=exist_ok, profile_name=profile)


def import_remote(name, host='https://export.dataset.sh/dataset', store_base=None, exist_ok=True, rename=None):
    manager = DatasetStorageManager(store_base=store_base)
    local_name = rename if rename is not None else name
    username, dataset = parse_dataset_name(local_name)
    remote_url = get_dataset_url_for_remote_host(host, name)
    manager.import_url(remote_url, username, dataset, exist_ok=exist_ok)


def exists(name, store_base=None):
    manager = DatasetStorageManager(store_base=store_base)
    username, dataset = parse_dataset_name(name)
    return manager.dataset_exist(username, dataset)


def delete_dataset(name, store_base=None):
    manager = DatasetStorageManager(store_base=store_base)
    username, dataset = parse_dataset_name(name)
    return manager.delete_dataset(username, dataset)


def modify_readme(name, readme, store_base=None):
    manager = DatasetStorageManager(store_base=store_base)
    username, dataset = parse_dataset_name(name)
    return manager.update_dataset_readme(username, dataset, readme)


def locate_file(name, store_base=None):
    manager = DatasetStorageManager(store_base=store_base)
    username, dataset = parse_dataset_name(name)
    return manager.get_dataset_file_path(username, dataset)


def list_datasets(store_base=None):
    manager = DatasetStorageManager(store_base=store_base)
    datasets = manager.list_datasets()
    return [f"{item.datastore}/{item.dataset}" for item in datasets.items]
