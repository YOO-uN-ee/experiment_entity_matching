import pygeohash
import polars as pl

pl_data = pl.read_csv('/home/yaoyi/pyo00005/Entity_Matching/dummy.csv', infer_schema_length=0)
print(pl_data.columns)

pl_data = pl_data.with_columns(
    pl.col(['latitude', 'longitude']).cast(pl.Float64)
).with_columns(
    location_hash = pl.struct(pl.col(['latitude', 'longitude'])).map_elements(lambda x: pygeohash.encode(latitude=x['latitude'], longitude=x['longitude'], precision=12))
)

print(pl_data['location_hash'])

lat, lon, precision = 41.88876, -87.63516, 12
hash_code = pygeohash.encode(latitude=lat, longitude=lon, precision=precision)

print(hash_code)