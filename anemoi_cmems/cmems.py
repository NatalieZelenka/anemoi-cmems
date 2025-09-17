import earthkit.data as ekd
import copernicusmarine

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

    def _download_data(self, dataset_id, param, start: datetime, end: datetime) -> xarray.Dataset:
        ds = copernicusmarine.open_dataset(
            dataset_id=dataset_id,
            variables=param,
            start_datetime=start,
            end_datetime=end,
            )

        return ds

    def _select_depth_levels(self, ds: ekd.FieldList, depth_index: list[int]) -> ekd.FieldList:
    
        depth_levels = [ds.depth.values[i-1] for i in depth_index]
        ds = ds.sel(depth=depth_levels)
        return ds

    def execute(self, dates: DateList, **kwargs) -> ekd.FieldList:
        param = self.config.get("param", [])

        dataset_id = self.config.get("dataset_id", None)
        if not dataset_id:
            raise ValueError("dataset_id is required")
    
        depth_indices = self.config.get("depth_indices", [])
        if not all([isinstance(d, int) for d in depth_indices]):
            raise ValueError("depth_indices must be a list of integers")
    
        if len(dates) != 0:
            start = dates[0]
            end = dates[-1]
        else:
            start = end = None  # For repeated_dates
            
        ds = self._download_data(
            dataset_id, 
            param, 
            start,
            end, 
        )

        if len(depth_indices) > 1:
            ds = self._select_depth_levels(ds, depth_indices)
            assert min(depth_indices) > 0, "depth_indices must be 1 or greater"
            assert max(depth_indices) <= 50, f"CMEMS has 50 depth levels, not {max(depth_indices)}"
            assert [int(d) for d in depth_indices] == depth_indices, "depth_indices must be integers"
        # TODO: Add rename with input print('\n'.join([f"{ds.depth.values[i]}: {i+1}" for i in range(len(ds.depth))]))
        


        return load_one("🌊", self.context, dates, ds)




