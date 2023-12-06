import json
import os
from typing import List, Optional
from pydantic import BaseModel, Field
from urllib.parse import urljoin


class DatasetDependencyItem(BaseModel):
    name: str
    rename: Optional[str] = None
    comment: Optional[str] = None
    host: Optional[str] = None

    def match_name(self, name):
        if self.rename is not None:
            return self.rename == name
        return self.name == name


class DatasetDependencies(BaseModel):
    datasets: List[DatasetDependencyItem] = Field(default_factory=list)

    def write_to_file(self, fp):
        with open(fp, 'w') as out:
            json.dump(
                self.model_dump(mode='json'),
                out,
                indent=4,
            )

    @staticmethod
    def read_from_file(fp):
        with open(fp) as f:
            return DatasetDependencies(**json.load(f))

    def has(self, name):
        for d in self.datasets:
            if d.match_name(name):
                return True
        return False

    def add_dataset(self, new_item):
        target_name = new_item.rename if new_item.rename is not None else new_item.name
        if self.has(target_name):
            raise ValueError('item exists')
        self.datasets.append(new_item)

    def remove(self, name):
        new_items = [item for item in self.datasets if not item.match_name(name)]
        self.datasets = new_items


def locate_dep_file(current_directory, max_it=30):
    file_name = 'dataset.list'
    it = 0
    while True:
        if file_name in os.listdir(current_directory):
            return os.path.abspath(os.path.join(current_directory, file_name))
        if current_directory == '/':
            return None
        current_directory = os.path.dirname(current_directory)
        it += 1
        if it >= max_it:
            return None


def get_dataset_url_for_remote_host(host, dataset):
    h = host
    if not h.endswith('/'):
        h = h + '/'
    absolute_url = urljoin(h, f'api/dataset/{dataset}/file')
    return absolute_url
