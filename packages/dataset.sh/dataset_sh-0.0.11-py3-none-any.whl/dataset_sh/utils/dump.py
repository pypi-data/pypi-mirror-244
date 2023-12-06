from dataset_sh import create
from dataset_sh.utils.misc import get_tqdm


def dump_single_collection(fn, name, data):
    with create(fn) as out:
        out.add_collection(name, data, data[0].__class__, tqdm=get_tqdm())


def dump_collections(fn, data_dict):
    tqdm = get_tqdm()
    with create(fn) as out:
        for name, data in tqdm(data_dict.items()):
            out.add_collection(name, data, data[0].__class__)
