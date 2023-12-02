import numpy as np

from aglio.data_manager import data_manager as _dm
from aglio.mapping import validate_lons


class Etopo(object):
    """
    class for loading dem topo files from
    https://www.ngdc.noaa.gov/mgg/global/global.html
    """

    def __init__(
        self, filename, loadFile: bool = True, use_negative_lons: bool = False
    ):

        self.filename = _dm.validate_file(filename)
        self.filetype = filename.split(".")[-1]
        self.topo = None
        self.latitude = None
        self.longitude = None
        self.topo_range = None
        self.use_negative_lons = use_negative_lons

        if loadFile:
            if self.filetype == "asc":
                self._load_gridded_ascii()
            else:
                raise NotImplementedError(f"filetype {self.filetype} not supported")

        return

    def _load_gridded_ascii(self):
        """loads the gridded etopo file"""

        # load the gridded data
        self.topo = np.loadtxt(self.filename, skiprows=5)

        # load the header
        headervals = []
        header = ["ncols", "nrows", "lon1", "lat1", "d_deg"]
        with open(self.filename, "r") as f:
            for _ in range(5):
                line = next(f)  # .next()
                headervals.append(float(line.split(" ")[-1]))
        header_dict = dict(zip(header, headervals))
        header_dict["lat2"] = (
            header_dict["lat1"] + header_dict["nrows"] * header_dict["d_deg"]
        )
        header_dict["lon2"] = (
            header_dict["lon1"] + header_dict["ncols"] * header_dict["d_deg"]
        )

        # calculate lat, lon arrays
        self.latitude = np.linspace(
            header_dict["lat2"], header_dict["lat1"], int(header_dict["nrows"])
        )
        raw_lons = np.linspace(
            header_dict["lon1"], header_dict["lon2"], int(header_dict["ncols"])
        )
        self.longitude = validate_lons(raw_lons, self.use_negative_lons)
        self.topo_range = header_dict
