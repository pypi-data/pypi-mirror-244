"""Main module."""
from typing import Dict, List, Optional, Type, Union

import numpy as np
import xarray as xr
from geopandas import GeoDataFrame
from scipy import spatial

import aglio.mapping as ygm
import aglio.seismology.datasets as sds
from aglio._utilities.dependencies import dependency_checker
from aglio._utilities.logger import aglio_log
from aglio.coordinate_transformations import geosphere2cart
from aglio.data_manager import data_manager as _dm
from aglio.point_data import _gpd_df_from_lat_lon
from aglio.seismology.collections import ProfileCollection


# aglio: sampling, binning, geopandas aggregate data
@xr.register_dataset_accessor("aglio")
class AglioAccessor:
    def __init__(self, xarray_obj):
        # __init__ can ONLY have xarray_obj here
        self._obj = xarray_obj
        self.crs = ygm.default_crs
        self.max_radius = ygm.default_radius
        self._interp_trees = {}
        self._has_neg_lons = np.any(self._obj.longitude < 0)

    def set_crs(self, new_crs):
        """sets the coordinate reference system (crs) for the dataset"""
        self.crs = new_crs

    _surface_gpd = None

    @property
    def surface_gpd(self):
        """a GeoDataFrame of the latitude, longitude points in the dataset"""
        if self._surface_gpd is None:
            lat, lg = self.latlon_grid
            lg = lg.ravel()
            lat = lat.ravel()
            df = _gpd_df_from_lat_lon(lat, lg, crs=self.crs)
            self._surface_gpd = df
        return self._surface_gpd

    _latlon_grid = None

    @property
    def latlon_grid(self):
        if self._latlon_grid is None:
            lon = self.get_coord("longitude")
            lat = self.get_coord("latitude")

            long, latg = np.meshgrid(lon, lat)
            self._latlon_grid = {"longitude": long, "latitude": latg}

        return self._latlon_grid["latitude"], self._latlon_grid["longitude"]

    def _validate_coord_name(self, name: str) -> str:
        if name in self._obj.coords:
            return name

        for candidate, aliases in coord_aliases.items():
            if name in aliases and candidate in self._obj.coords:
                return candidate
        raise RuntimeError(
            f"Could not find {name} coordinate or equivalent in dataset. If it "
            f"exists by another name, add it to the aglio.coord_aliases"
            f" dictionary."
        )

    def get_coord(self, name: str, copy: bool = True):
        """
        get a coordinate array, accounting for coordinate aliases

        Parameters
        ----------
        name: str
            the coordinate name
        copy: bool
            (optional) return a copy of the array, default True

        Returns
        -------
        ArrayLike
            np.ndarray or a xr.DataArray of coordinate values
        """
        name = self._validate_coord_name(name)
        coord = self._obj[name]
        if copy:
            coord = coord.copy()
        if name in coord_aliases["longitude"]:
            coord = ygm.validate_lons(coord.values)
        return coord

    def filter_surface_gpd(
        self,
        df_gpds: Union[List[GeoDataFrame], GeoDataFrame],
        drop_null=False,
        drop_inside=False,
    ):
        """
        filter the surface points of the dataset with GeoDataFrame

        Parameters
        ----------
        df_gpds: GeoDataFrame or list of GeoDataFrames
            a single GeoDataFrame or list of GeoDataFrames to use for filtering.
        drop_null: bool
            drop any null values from the resulting dataframe, effectively
            dropping points falling outside of df_gpds
        drop_inside: bool
            drop any points that fall within df_gpds bounds

        Note that drop_null and drop_inside are applied to all successive joins
        if df_gpds is a list of GeoDataFrames.

        Returns
        -------
        GeoDataFrame
            a dataframe for the ds.aglio.surface_points filtered by df_gpds

        """
        df = self.surface_gpd
        return ygm.successive_joins(
            df, df_gpds, drop_null=drop_null, drop_inside=drop_inside
        )

    def get_profiles(
        self,
        field: str,
        df_gpds: Union[List[GeoDataFrame], GeoDataFrame] = None,
        vertical_mask=None,
        drop_null: bool = False,
        drop_inside: bool = False,
    ) -> ProfileCollection:
        """
        extract a collection of 1d profiles

        Parameters
        ----------
        field: str
            the field to extract 1d profiles from
        df_gpds: GeoDataFrame or list of GeoDataFrames
            (optional) if present, will filter the surface points to return only
            the profiles falling within (or without) df_gpds
        vertical_mask: ArrayLike
            a boolean mask to apply to along the vertical coordinate of 1d profiles
        drop_null: bool
            (optional) drop any null values from the resulting dataframe,
            dropping points falling outside of df_gpds. Only used if df_gpds is
            present.
        drop_inside: bool
            (optional) drop any points that fall within df_gpds bounds. Only used
            if df_gpds is present.


        Returns
        -------
        ProfileCollection

        """
        var = getattr(self._obj, field)
        vert_name = _get_vertical_coord_name(var)
        vertical_sel = {}
        if vertical_mask is not None:
            depth = _get_vertical_coord(var)
            vertical_sel[vert_name] = depth[vertical_mask]

        if df_gpds is not None:
            # find the surface points falling within the provided dataframe
            surface_df = self.filter_surface_gpd(
                df_gpds,
                drop_null=drop_null,
                drop_inside=drop_inside,
            )
            lons = surface_df.longitude.to_xarray()
            lats = surface_df.latitude.to_xarray()
            if self._has_neg_lons:
                # surface_df will be 0, 360 always, offset values
                lon_mask = lons > 180.0
                lons[lon_mask] = lons[lon_mask] - 360.0
                del lon_mask
            sel_dict = {}
            sel_dict["longitude"] = lons
            sel_dict["latitude"] = lats
            fvars = var.sel(sel_dict)
            fvars = fvars.sel(vertical_sel)
            lon_vals = fvars.longitude.values
            lat_vals = fvars.latitude.values
            depth_vals = getattr(fvars, vert_name).values
            fvars = fvars.transpose("index", vert_name).values
        else:
            fvars = var.sel(vertical_sel)
            depth_vals = fvars.depth.values

            # combine the lat/lon grid into 1d dimension then reorder to ensure
            # depth first and extract the 2d array
            fvars = fvars.stack(surface_pts=("latitude", "longitude"))
            fvars = fvars.transpose("surface_pts", vert_name)
            lon_vals = fvars.longitude.values
            lat_vals = fvars.latitude.values
            fvars = fvars.values

        return ProfileCollection(
            fvars,
            depth_vals,
            lon_vals,
            lat_vals,
            crs=self.crs,
        )

    _cartesian_coords = None

    @property
    def cartesian_coords(self) -> tuple:
        """
        returns 3d arrays representing earth-centered cartesian coordinates of
        every grid point
        """

        if self._cartesian_coords is None:
            depth, lat, lon = self._get_lat_lon_depth_grid()
            radius = self.max_radius - depth
            x, y, z = geosphere2cart(lat, lon, radius)
            self._cartesian_coords = x, y, z

        return self._cartesian_coords

    def _get_lat_lon_depth_grid(self):

        vert_coord = _get_vertical_coord_name(self._obj)
        depth_ = self.get_coord(vert_coord)
        lat_ = self.get_coord("latitude")
        lon_ = self.get_coord("longitude")
        depth, lat, lon = np.meshgrid(depth_, lat_, lon_, indexing="ij")
        return depth, lat, lon

    _cartesian_bbox = None

    @property
    def cartesian_bbox(self):
        if self._cartesian_bbox is None:
            x, y, z = self.cartesian_coords
            cbbox = np.array([[d.min(), d.max()] for d in [x, y, z]])
            self._cartesian_bbox = cbbox
        return self._cartesian_bbox

    def interpolate_to_uniform_cartesian(
        self,
        fields: List[str],
        N: Optional[int] = 50,
        max_dist: Optional[Union[int, float]] = 100,
        interpChunk: Optional[int] = 500000,
        recylce_trees: Optional[bool] = False,
        return_yt: Optional[bool] = False,
        rescale_coords: Optional[bool] = False,
        apply_functions: Optional[dict] = None,
        subselect_bbox: Optional[Dict[str, Union[tuple, list]]] = None,
    ):
        """
        moves geo-spherical data (radius/depth, lat, lon) to earth-centered
        cartesian coordinates using a kdtree with inverse distance weighting (IDW)

        fields: List[str]
            fields to interpolate
        N: int
            number of points in shortest dimension (default 50)
        max_dist : int or float
            the max distance away for nearest neighbor search (default 100)
        interpChunk : int
            the chunk size for querying the kdtree (default 500000)
        recylce_trees : bool
            if True, will store the generated kdtree(s) in memory (default False)
        return_yt: bool
            if True, will return a yt dataset (default False)
        rescale_coords: bool
            if True, will rescale the dimensions to 1. in smallest range,
            maintaining aspect ratio in other dimensions (default False)
        apply_functions: dict
            a dictionary with fields as keys, pointing to a list of callable
            functions that get applied to the interpolated field. Functions
            must accept and return an ndarray.
        subselect_bbox: dict
            bounds of a subselection (optional).
            {'latitude': [minlat, maxlat],
             'longitude': [minlon, maxlon]
             'radius': [minradius, maxradius]
            }
        """

        # check yt first if it is being used
        if return_yt is True:
            if dependency_checker.has_yt is False:
                raise RuntimeError("this functionality requires yt.")

        # set the bounding cartesian box of the interpolated grid
        if subselect_bbox:
            for k, v in subselect_bbox.items():
                subselect_bbox[k] = np.asarray(v)
                xb, yb, zb = geosphere2cart(
                    subselect_bbox["latitude"],
                    subselect_bbox["longitude"],
                    subselect_bbox["radius"],
                )
            cart_bbox = np.array([[d.min(), d.max()] for d in [xb, yb, zb]])
        else:
            cart_bbox = self.cartesian_bbox

        full_cart_bbox = self.cartesian_bbox
        full_wids = np.abs(full_cart_bbox[:, 1] - full_cart_bbox[:, 0])

        if apply_functions is None:
            apply_functions = {}

        x, y, z = self.cartesian_coords  # the actual xyz at which we have data

        # drop points at which we don't have data
        wids = np.abs(cart_bbox[:, 1] - cart_bbox[:, 0])
        dx = wids.min() / N
        Ngrid = np.floor(wids / dx).astype(int)

        fillval = np.nan
        xdata = x.ravel()
        ydata = y.ravel()
        zdata = z.ravel()
        trees = {}
        interpd = {}
        for field in fields:
            data = getattr(self._obj, field).values.ravel()

            if recylce_trees and field in self._interp_trees:
                trees[field] = self._interp_trees[field]
            else:
                dmask = data != fillval
                x_fi = (xdata[dmask] - full_cart_bbox[0][0]) / full_wids[0]
                y_fi = (ydata[dmask] - full_cart_bbox[1][0]) / full_wids[1]
                z_fi = (zdata[dmask] - full_cart_bbox[2][0]) / full_wids[2]
                data = data[data != fillval]
                xyz = np.column_stack((x_fi, y_fi, z_fi))
                aglio_log.info("building kd tree for " + field)
                trees[field] = {"tree": spatial.cKDTree(xyz), "data": data}
                aglio_log.info("... kd tree built")

            interpd[field] = np.full((Ngrid[0], Ngrid[1], Ngrid[2]), np.nan)

        # interpolate the field data from x, y, z to xyz_int
        xyz = [
            np.linspace(cart_bbox[d, 0], cart_bbox[d, 1], Ngrid[d]) for d in range(3)
        ]
        xdata, ydata, zdata = np.meshgrid(*xyz, indexing="ij")
        orig_shape = xdata.shape
        xdata = xdata.ravel(order="C")
        ydata = ydata.ravel(order="C")
        zdata = zdata.ravel(order="C")

        parallel_query = False
        if parallel_query:
            raise NotImplementedError
        else:
            nxdata = (xdata - full_cart_bbox[0][0]) / full_wids[0]
            nydata = (ydata - full_cart_bbox[1][0]) / full_wids[1]
            nzdata = (zdata - full_cart_bbox[2][0]) / full_wids[2]

            # kd-tree max dists is sum over all kdtree dimensions, calculate
            # allowable dist assume same physical dist in each dimension
            # this is needed since we rescaled the kdtree from 0 to 1 in every
            # dimension
            max_dists = np.array([max_dist / full_wids[i] for i in range(3)])
            nmax_dist = np.sqrt(np.sum(max_dists * max_dists))

            interpd = _query_trees(
                nxdata,
                nydata,
                nzdata,
                interpChunk,
                fields,
                trees,
                interpd,
                orig_shape,
                nmax_dist,
            )

        if recylce_trees:
            self._interp_trees.update(trees)

        if rescale_coords:
            max_wid = wids.max()
            for dim in range(3):
                xyz[dim] = (xyz[dim] - cart_bbox[dim, 0]) / max_wid

        for key, funchandles in apply_functions.items():
            for funchandle in funchandles:
                interpd[key] = funchandle(interpd[key])

        if return_yt:
            import yt  # noqa

            shp = interpd[fields[0]].shape
            n_cart_bbox = np.zeros((3, 2))
            for dim in range(3):
                n_cart_bbox[dim][0] = xyz[dim].min()
                n_cart_bbox[dim][1] = xyz[dim].max()

            return yt.load_uniform_grid(interpd, shp, bbox=n_cart_bbox)

        if len(interpd) == 1:
            interpd = interpd[fields[0]]
        return xyz[0], xyz[1], xyz[2], interpd

    def _perturbation_calcs(
        self,
        ref_model: Union[Type[sds.ReferenceModel1D], Type[sds.ReferenceCollection]],
        field: str,
        ref_model_field: str = None,
        perturbation_type: str = "percent",
        to_perturbation: bool = True,
    ):

        field_data = getattr(self._obj, field)
        depth, lat, lon = self._get_lat_lon_depth_grid()

        if type(ref_model) == sds.ReferenceModel1D:
            # evaluate interpolated reference model at depths
            ref_data = ref_model.evaluate(depth)
        elif type(ref_model) == sds.ReferenceCollection:
            model = getattr(ref_model, ref_model_field)
            ref_data = model.evaluate(depth)

        if to_perturbation:
            # field is in reference, calculate the perturbation
            return_data = sds._calculate_perturbation(
                ref_data, field_data, perturbation_type
            )
        else:
            # calculate absolute from perturbation
            return_data = sds._calculate_absolute(
                ref_data, field_data, perturbation_type
            )

        return return_data

    def get_perturbation(
        self,
        ref_model: Union[Type[sds.ReferenceModel1D], Type[sds.ReferenceCollection]],
        field: str,
        ref_model_field: Optional[str] = None,
        perturbation_type: Optional[str] = "percent",
    ) -> np.ndarray:
        """
        Calculate a perturbation from a 1D reference model

        Parameters
        ----------
        ref_model:
            the reference model, should be either a ReferenceModel1D or
            ReferenceCollection instance
        field: str
            the data field to calculate a perturbation for
        ref_model_field: str
            (optional) the field in the reference model to use. defaults to the
            value of the field parameter
        perturbation_type: str
            (optional) either "percent" or "absolute", defaults to "percent"

        Returns
        -------
        np.ndarray
            array of perturbation values
        """

        return self._perturbation_calcs(
            ref_model,
            field,
            ref_model_field=ref_model_field,
            perturbation_type=perturbation_type,
            to_perturbation=True,
        )

    def get_absolute(
        self,
        ref_model: Union[Type[sds.ReferenceModel1D], Type[sds.ReferenceCollection]],
        field: str,
        ref_model_field: str = None,
        perturbation_type: str = "percent",
    ):
        """
        Calculate an absolute value from a perturbation field for a 1D reference
        model

        Parameters
        ----------
        ref_model:
            the reference model, should be either a ReferenceModel1D or
            ReferenceCollection instance
        field: str
            the perturbation field to calculate absolute values from
        ref_model_field: str
            (optional) the field in the reference model to use. defaults to the
            value of the field parameter
        perturbation_type: str
            (optional) either "percent" or "absolute", defaults to "percent"

        Returns
        -------
        np.ndarray
            array of absolute values
        """
        return self._perturbation_calcs(
            ref_model,
            field,
            ref_model_field=ref_model_field,
            perturbation_type=perturbation_type,
            to_perturbation=False,
        )


def _query_trees(
    xdata: np.ndarray,
    ydata: np.ndarray,
    zdata: np.ndarray,
    interpChunk: int,
    fields: List[str],
    trees: dict,
    interpd: dict,
    orig_shape: tuple,
    max_dist: float,
) -> dict:
    # query the tree at each new grid point and weight nearest neighbors
    # by inverse distance. proceed in chunks.
    N_grid = len(xdata)
    N_chunks = int(N_grid / interpChunk) + 1
    aglio_log.info(f"querying kdtree on interpolated grid in {N_chunks} chunks")
    for i_chunk in range(0, N_chunks):
        aglio_log.info(f"   processing chunk {i_chunk + 1} of {N_chunks}")
        i_0 = i_chunk * interpChunk
        i_1 = i_0 + interpChunk
        if i_1 > N_grid:
            i_1 = N_grid
        pts = np.column_stack((xdata[i_0:i_1], ydata[i_0:i_1], zdata[i_0:i_1]))
        indxs = np.array(range(i_0, i_1))  # the linear indeces of this chunk
        for fi in fields:
            (dists, tree_indxs) = trees[fi]["tree"].query(
                pts, k=8, distance_upper_bound=max_dist
            )

            # remove points with all infs (no NN's within max_dist)
            m = np.all(~np.isinf(dists), axis=1)
            tree_indxs = tree_indxs[m]
            indxs = indxs[m]
            dists = dists[m]

            # IDW with array manipulation
            # Build weighting matrix
            wts = 1 / dists
            wts = wts / np.sum(wts, axis=1)[:, np.newaxis]  # shape (N,8)
            vals = trees[fi]["data"][tree_indxs]  # shape (N,8)
            vals = vals * wts
            vals = np.sum(vals, axis=1)  # shape (N,)

            # store in proper indeces
            full_indxs = np.unravel_index(indxs, orig_shape, order="C")
            interpd[fi][full_indxs] = vals

    return interpd


_latnames = ["lat", "latitude", "lats"]
_lonnames = ["lon", "long", "longitude", "lons"]
coord_aliases = {}
for ref_name, aliases in zip(["latitude", "longitude"], [_latnames, _lonnames]):
    full_list = (
        aliases + [a.upper() for a in aliases] + [a.capitalize() for a in aliases]
    )
    coord_aliases[ref_name] = full_list
coord_aliases["depth"] = ["depth"]


def open_dataset(file, *args, **kwargs):
    """
    opens a dataset with xr.open_dataset after validating filename

    Parameters
    ----------
    file:
        the filename
    *args, **kwargs: any additional arguments passed to xr.open_dataset

    Returns
    -------
    open xarray dataset handle

    """
    file = _dm.validate_file(file)
    return xr.open_dataset(file, *args, **kwargs)


def _get_vertical_coord_name(x: Union[xr.DataArray, xr.Dataset]) -> str:
    the_vert = None
    for dim in x.dims:
        if dim not in coord_aliases["latitude"] + coord_aliases["longitude"]:
            the_vert = dim
    if the_vert is None:
        raise ValueError("Could not determine vertical coordinate.")
    return the_vert


def _get_vertical_coord(x: Union[xr.DataArray, xr.Dataset]):
    vert_name = _get_vertical_coord_name(x)
    return getattr(x, vert_name)
