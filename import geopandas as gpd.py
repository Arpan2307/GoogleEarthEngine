import geopandas as gpd
import xarray as xr
import rasterio.mask

# Specify the path to the NetCDF file
nc_path = r'C:\GEE project\Singapore\MYD11A2.061_1km_aid0001.nc'

# Read the NetCDF file
ds = xr.open_dataset(nc_path)

# Load the shapefile
shapefile_path = r"C:\Users\arpan\Downloads\data\SGP_adm1.shp"
gdf = gpd.read_file(shapefile_path)

# Convert the geopandas dataframe to the same CRS as the NetCDF data
gdf = gdf.to_crs(ds.rio.crs)

# Convert the geopandas dataframe to a rasterio geometry
gdf_geom = gpd.to_raster(gdf, ds.rio.transform)

# Use the rasterio geometry to mask the NetCDF data
masked_data, _ = rasterio.mask.mask(ds, gdf_geom, crop=True)

# Save the masked data as a new NetCDF file
masked_ds = xr.DataArray(masked_data, dims=ds.dims, coords=ds.coords)
masked_ds.to_netcdf('masked_output.nc')
