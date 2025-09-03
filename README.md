# anemoi-cmems

Prototype plugin created using `anemoi-plugins` for creating an anemoi dataset using `copernicusmarine` API - see [`anemoi-datasets-configs/issues/116`](https://github.com/ecmwf/anemoi-datasets-configs/issues/116)

In order to run this script you must first:
1. register as a Copernicus Marine user.
2. In the command line, run `copernicusmarine login` and enter your user name and password, which will store your credentials locally in a `.copernicusmarine-credentials` file.
3. Install this plugin `pip install -e .`

## Local changes to `anemoi-datasets`:

At the current time I'm using a local copy of `anemoi-datasets` which has the following changes to enable the tests to run:
- An empty `TestingContext` in `src/datasets/create/testing.py` as in [this PR](https://github.com/ecmwf/anemoi-datasets/pull/408)
- The following change in `src/anemoi/datasets/create/sources/xarray_support/__init__.py`:
    ```
    -    data = xr.open_dataset(dataset, **options)
    +    if isinstance(dataset, xr.Dataset):
    +        data = dataset
    +    else: 
    +        data = xr.open_dataset(dataset, **options)
    ```

## Tests
