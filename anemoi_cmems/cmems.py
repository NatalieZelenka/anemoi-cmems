import earthkit.data as ekd
import copernicusmarine

from typing import Any
import xarray
from datetime import datetime

from anemoi.datasets.create.source import Source
from anemoi.datasets.create.typing import DateList
from anemoi.datasets.create.sources.xarray import load_one


class CmemsPlugin(Source):

    # The version of the plugin API, used to ensure compatibility
    # with the plugin manager.

    api_version = "1.0.0"

    # The schema of the plugin, used to validate the parameters.
    # This is a Pydantic model.

    schema = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = kwargs
        self.flavour = None
        self.patch = None

    def _download_data(self, dataset_id, param, start: datetime, end: datetime, min_depth, max_depth) -> xarray.Dataset:
        ds = copernicusmarine.open_dataset(
            dataset_id=dataset_id,
            variables=param,
            start_datetime=start,
            end_datetime=end,
            minimum_depth=min_depth,
            maximum_depth=max_depth,
            )
        return ds

    def _select_depth_levels(self, ds: ekd.FieldList, depth_levels: list[int]) -> ekd.FieldList:
        ds = ds.sel(depth=depth_levels, method='nearest')
        return ds

    def execute(self, dates: DateList, **kwargs) -> ekd.FieldList:
        param = self.config.get("param", [])      

        dataset_id = self.config.get("dataset_id", None)
        if not dataset_id:
            raise ValueError("dataset_id is required")

        depth_levels = self.config.get("depth_levels", [])
        if not all([isinstance(d, int) for d in depth_levels]):
            raise ValueError("depth_levels must be a list of integers")
        
        depth_levels.sort()
        if len(depth_levels) != 0:
            min_depth = max_depth = None
        else:
            min_depth = depth_levels[0]
            max_depth = depth_levels[-1]

        # TODO: is datelist sorted?
        ds = self._download_data(
            dataset_id, 
            param, 
            dates[0],
            dates[-1], 
            min_depth, 
            max_depth,
        )

        if len(depth_levels) > 1:
            ds = self._select_depth_levels(ds, depth_levels)

        return load_one("🌊", self.context, dates, ds)




