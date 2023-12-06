import datetime
import json
import os
import warnings
from dataclasses import dataclass
from typing import List, Optional

from pydantic import BaseModel, Field, ValidationError


class DatasetClientProfile(BaseModel):
    host: str
    key: str
    name: Optional[str] = None


class DatasetClientProfileConfig(BaseModel):
    profiles: List[DatasetClientProfile] = Field(default_factory=list)

    @staticmethod
    def load_profiles():
        config_file = DatasetClientProfileConfig.get_profile_file_path()
        if os.path.exists(config_file):
            with open(config_file) as fd:
                try:
                    json_config = json.load(fd)
                    ret = DatasetClientProfileConfig(**json_config)
                    return ret
                except (ValidationError, json.decoder.JSONDecodeError):
                    warnings.warn('cannot parse profile config')
        return DatasetClientProfileConfig()

    def find_matching_profile(self, url, profile_name=None):
        if profile_name is not None:
            for p in self.profiles:
                if p.name == profile_name:
                    return p
        else:
            for p in self.profiles:
                if url.startswith(p.host):
                    return p

    def save(self):
        config_file = DatasetClientProfileConfig.get_profile_file_path()
        data = self.model_dump(mode='json')
        with open(config_file, 'w') as out:
            json.dump(data, out, indent=4)

    def add_profile(self, host, key, name=None):
        p = DatasetClientProfile(host=host, key=key, name=name)
        self.profiles.append(p)
        return self

    @staticmethod
    def get_profile_file_path():
        config_file = os.path.expanduser('~/.dataset.sh.profile.json')
        return config_file


@dataclass
class DatasetInfo:
    name: str
    is_redirect: bool


class DatasetInfoSnippet(BaseModel):
    datastore: str
    dataset: str
    readme: str


class NamespaceList(BaseModel):
    stores: List[str]


class DatasetListingResults(BaseModel):
    items: List[DatasetInfoSnippet]


class SourceInfo(BaseModel):
    url: str
    download_time: datetime.datetime = Field(default_factory=datetime.datetime.now)


class DatasetHomeFolderFilenames:
    MARKER = '.dataset.marker'
    META = 'meta.json'
    DATA_FILE = 'file'
    README = 'readme.md'
    REMOTE_SOURCE = 'remote_source.json'  # if this file is downloaded from a remote source,


class DatasetFileInternalPath:
    BINARY_FOLDER = 'bin'
    COLLECTION_FOLDER = 'coll'

    META_FILE_NAME = 'meta.json'
    DATA_FILE = 'data.jsonl'


@dataclass
class DatasetHomeFolder:
    base: str
    name: Optional[str] = None

    def meta(self):
        return os.path.join(self.base, DatasetHomeFolderFilenames.META)

    def marker(self):
        return os.path.join(self.base, DatasetHomeFolderFilenames.MARKER)

    def datafile(self):
        return os.path.join(self.base, DatasetHomeFolderFilenames.DATA_FILE)

    def readme(self):
        return os.path.join(self.base, DatasetHomeFolderFilenames.README)

    def marker_exist(self):
        return os.path.isfile(self.marker())

    def remote_source(self):
        return os.path.join(self.base, DatasetHomeFolderFilenames.REMOTE_SOURCE)

    def code_example(self, collection_name):
        return os.path.join(self.base, f'usage_code_{collection_name}.py')

    def sample_file(self, collection_name):
        return os.path.join(self.base, f'data_sample_{collection_name}.jsonl')
