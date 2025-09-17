from anemoi.datasets.create.sources import create_source
from anemoi.datasets.create.testing import TestingContext
from anemoi.datasets.create import creator_factory

import os
import pytest

ROOTDIR = os.path.dirname(os.path.dirname(__file__))

def test_plugin():
    source = create_source(TestingContext, "cmems")
    assert source is not None

@pytest.mark.skip(reason="Long test, only run manually")
def test_with_yaml():
    config = os.path.join(ROOTDIR, 'example.yaml')
    output = os.path.join(ROOTDIR, 'example.zarr')

    creator_factory("init", config=config, path=output, overwrite=True).run()
    creator_factory("load", path=output).run()
    creator_factory("finalise", path=output).run()
    creator_factory("patch", path=output).run()
    creator_factory("cleanup", path=output).run()
    creator_factory("verify", path=output).run()

if __name__ == "__main__":
   test_with_yaml()
