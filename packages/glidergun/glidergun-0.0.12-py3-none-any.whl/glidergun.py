""" Map Algebra with NumPy and Rasterio """
import dataclasses
import IPython
import numpy as np
import rasterio
from base64 import b64encode
from dataclasses import dataclass
from io import BytesIO
from matplotlib import pyplot
from numpy import arctan, arctan2, cos, gradient, ndarray, pi, sin, sqrt
from numpy.lib.stride_tricks import as_strided
from rasterio.crs import CRS
from rasterio.drivers import driver_from_extension
from rasterio.transform import Affine, from_bounds
from rasterio.warp import reproject, Resampling
from typing import Callable, Literal, Optional, Tuple, Union


# Types

ColorMap = Literal[
    "Accent",
    "afmhot",
    "autumn",
    "binary",
    "Blues",
    "bone",
    "BrBG",
    "brg",
    "BuGn",
    "BuPu",
    "bwr",
    "cividis",
    "CMRmap",
    "cool",
    "coolwarm",
    "copper",
    "cubehelix",
    "Dark2",
    "flag",
    "gist_earth",
    "gist_gray",
    "gist_heat",
    "gist_ncar",
    "gist_rainbow",
    "gist_stern",
    "gist_yarg",
    "GnBu",
    "gnuplot",
    "gnuplot2",
    "gray",
    "Greens",
    "Greys",
    "hot",
    "hsv",
    "inferno",
    "jet",
    "magma",
    "nipy_spectral",
    "ocean",
    "Oranges",
    "OrRd",
    "Paired",
    "Pastel1",
    "Pastel2",
    "pink",
    "PiYG",
    "plasma",
    "PRGn",
    "prism",
    "PuBu",
    "PuBuGn",
    "PuOr",
    "PuRd",
    "Purples",
    "rainbow",
    "RdBu",
    "RdGy",
    "RdPu",
    "RdYlBu",
    "RdYlGn",
    "Reds",
    "seismic",
    "Set1",
    "Set2",
    "Set3",
    "Spectral",
    "spring",
    "summer",
    "tab10",
    "tab20",
    "tab20b",
    "tab20c",
    "terrain",
    "turbo",
    "twilight",
    "twilight_shifted",
    "viridis",
    "winter",
    "Wistia",
    "YlGn",
    "YlGnBu",
    "YlOrBr",
    "YlOrRd",
]

DataType = Literal[
    "float32",
    "float64",
    "int8",
    "int16",
    "int32",
    "int64",
    "uint8",
    "uint16",
    "uint32",
    "uint64",
]


class Extent(Tuple[float, float, float, float]):
    def __new__(cls, xmin: float, ymin: float, xmax: float, ymax: float):
        return super(Extent, cls).__new__(cls, (xmin, ymin, xmax, ymax))

    def intersect(self, extent: "Extent"):
        return Extent(*[f(x) for f, x in zip((max, max, min, min), zip(self, extent))])

    def union(self, extent: "Extent"):
        return Extent(*[f(x) for f, x in zip((min, min, max, max), zip(self, extent))])

    __and__ = intersect
    __rand__ = __and__
    __or__ = union
    __ror__ = __or__


Operand = Union["Grid", float, int]


@dataclass(frozen=True)
class Grid:
    data: ndarray
    crs: CRS
    transform: Affine
    nodata: Optional[float]
    _cmap: ColorMap = "gray"

    def __post_init__(self):
        self.data.flags.writeable = False

    # Properties

    @property
    def width(self) -> int:
        return self.data.shape[1]

    @property
    def height(self) -> int:
        return self.data.shape[0]

    @property
    def dtype(self) -> DataType:
        return str(self.data.dtype)  # type: ignore

    @property
    def is_float(self) -> float:
        return self.dtype.startswith("float")

    @property
    def xmin(self) -> float:
        return self.transform.c

    @property
    def ymin(self) -> float:
        return self.ymax + self.height * self.transform.e

    @property
    def xmax(self) -> float:
        return self.xmin + self.width * self.transform.a

    @property
    def ymax(self) -> float:
        return self.transform.f

    @property
    def extent(self) -> Extent:
        return Extent(self.xmin, self.ymin, self.xmax, self.ymax)

    @property
    def min(self) -> float:
        return np.nanmin(self.data)

    @property
    def max(self) -> float:
        return np.nanmax(self.data)

    @property
    def cell_size(self) -> float:
        return self.transform.a

    def _create(self, data: ndarray):
        return Grid(
            data,
            self.crs,
            self.transform,
            self.nodata,
            self._cmap,
        )

    def _data(self, n: Operand):
        if isinstance(n, Grid):
            return n.data
        return n

    def _apply(self, left: Operand, right: Operand, op: Callable):
        if not isinstance(left, Grid) or not isinstance(right, Grid):
            return self._create(op(self._data(left), self._data(right)))

        if left.cell_size == right.cell_size and left.extent == right.extent:
            return self._create(op(left.data, right.data))

        extent = left.extent & right.extent

        l_adjusted = left.clip(extent).change_type(self.dtype)
        r_adjusted = right.resample(self.cell_size).clip(extent).change_type(self.dtype)

        return self._create(op(l_adjusted.data, r_adjusted.data))

    # Operators

    def __add__(self, n: Operand):
        return self._apply(self, n, np.add)

    __radd__ = __add__

    def __sub__(self, n: Operand):
        return self._apply(self, n, np.subtract)

    def __rsub__(self, n: Operand):
        return self._apply(n, self, np.subtract)

    def __mul__(self, n: Operand):
        return self._apply(self, n, np.multiply)

    __rmul__ = __mul__

    def __pow__(self, n: Operand):
        return self._apply(self, n, np.power)

    def __rpow__(self, n: Operand):
        return self._apply(n, self, np.power)

    def __truediv__(self, n: Operand):
        return self._apply(self, n, np.true_divide)

    def __rtruediv__(self, n: Operand):
        return self._apply(n, self, np.true_divide)

    def __floordiv__(self, n: Operand):
        return self._apply(self, n, np.floor_divide)

    def __rfloordiv__(self, n: Operand):
        return self._apply(n, self, np.floor_divide)

    def __mod__(self, n: Operand):
        return self._apply(self, n, np.mod)

    def __rmod__(self, n: Operand):
        return self._apply(n, self, np.mod)

    def __lt__(self, n: Operand):
        return self._apply(self, n, np.less)

    def __gt__(self, n: Operand):
        return self._apply(self, n, np.greater)

    __rlt__ = __gt__

    __rgt__ = __lt__

    def __le__(self, n: Operand):
        return self._apply(self, n, np.less_equal)

    def __ge__(self, n: Operand):
        return self._apply(self, n, np.greater_equal)

    __rle__ = __ge__

    __rge__ = __le__

    def __eq__(self, n: Operand):
        return self._apply(self, n, np.equal)

    __req__ = __eq__

    def __ne__(self, n: Operand):
        return self._apply(self, n, np.not_equal)

    __rne__ = __ne__

    def __and__(self, n: Operand):
        return self._apply(self, n, np.bitwise_and)

    __rand__ = __and__

    def __or__(self, n: Operand):
        return self._apply(self, n, np.bitwise_or)

    __ror__ = __or__

    def __xor__(self, n: Operand):
        return self._apply(self, n, np.bitwise_xor)

    def __rxor__(self, n: Operand):
        return self._apply(n, self, np.bitwise_xor)

    def __rshift__(self, n: Operand):
        return self._apply(self, n, np.right_shift)

    def __lshift__(self, n: Operand):
        return self._apply(self, n, np.left_shift)

    __rrshift__ = __lshift__

    __rlshift__ = __rshift__

    def __neg__(self):
        return self._create(-1 * self.data)

    def __pos__(self):
        return self._create(1 * self.data)

    def __invert__(self):
        return con(self, False, True)

    def __repr__(self):
        d = 3 if self.is_float else 0
        return (
            f"{self.width} x {self.height} {self.dtype} ({self.min:.{d}f} ~ {self.max:.{d}f}) {self.crs}"
            + f" Cell:{self.cell_size}"
        )

    def isnan(self):
        return self.local(np.isnan)

    def local(self, func: Callable[[ndarray], ndarray]):
        return self._create(func(self.data))

    def _get_blocks(self, buffer: int):
        row = np.zeros((buffer, self.width)) * np.nan
        col = np.empty((self.height + 2 * buffer, buffer)) * np.nan
        array = np.hstack([col, np.vstack([row, self.data, row]), col])
        window = (2 * buffer + 1, 2 * buffer + 1)
        shape = tuple(np.subtract(array.shape, window) + 1) + window
        return as_strided(array, shape, array.strides * 2)

    def focal(self, func: Callable[[ndarray], Union[float, int]], buffer: int = 1):
        blocks = self._get_blocks(buffer)
        return self._create(np.array([list(map(func, block)) for block in blocks]))

    def focal_mean(self, buffer=1):
        return self.focal(np.mean, buffer)

    def focal_std(self, buffer=1):
        return self.focal(np.std, buffer)

    def focal_min(self, buffer=1):
        return self.focal(np.min, buffer)

    def focal_max(self, buffer=1):
        return self.focal(np.max, buffer)

    def focal_sum(self, buffer=1):
        return self.focal(np.sum, buffer)

    def reproject(
        self,
        extent: Tuple[float, float, float, float],
        cell_size: float,
        resampling: Resampling,
    ):
        grid = self.to_int16() if self.dtype == "bool" else self

        (xmin, ymin, xmax, ymax) = extent
        xoff = (xmin - grid.xmin) / grid.transform.a
        yoff = (ymax - grid.ymax) / grid.transform.e

        scaling = cell_size / grid.cell_size

        dst_transform = (
            grid.transform * Affine.translation(xoff, yoff) * Affine.scale(scaling)
        )
        destination = (
            np.zeros(
                (
                    int(round((ymax - ymin) / abs(grid.transform.e)) / scaling),
                    int(round((xmax - xmin) / abs(grid.transform.a)) / scaling),
                ),
                grid.dtype,
            )
            * np.nan
        )

        reproject(
            source=grid.data,
            destination=destination,
            src_transform=grid.transform,
            src_crs=grid.crs,
            src_nodata=grid.nodata,
            dst_transform=dst_transform,
            dst_crs=grid.crs,
            dst_nodata=grid.nodata,
            resampling=resampling,
        )

        result = Grid(destination, grid.crs, dst_transform, grid.nodata, grid._cmap)

        return con(result == result.nodata, np.nan, result)

    def clip(self, extent: Tuple[float, float, float, float]):
        return self.reproject(extent, self.cell_size, Resampling.nearest)

    def resample(self, cell_size: float, resampling: Resampling = Resampling.nearest):
        return self.reproject(self.extent, cell_size, resampling)

    def abs(self):
        return self.local(np.abs)

    def random(self):
        return self._create(np.random.rand(self.height, self.width))

    def round(self, decimals: int = 0):
        return self.local(lambda data: np.round(data, decimals))

    def aspect(self):
        x, y = gradient(self.data)
        return self._create(arctan2(-x, y))

    def slope(self):
        x, y = gradient(self.data)
        return self._create(pi / 2.0 - arctan(sqrt(x * x + y * y)))

    def hillshade(self, azimuth: float = 315, altitude: float = 45):
        azimuth = azimuth * pi / 180.0
        altitude = altitude * pi / 180.0

        aspect = self.aspect().data
        slope = self.slope().data

        shaded = sin(altitude) * sin(slope) + cos(altitude) * cos(slope) * cos(
            azimuth - aspect
        )

        return self._create((255 * (shaded + 1) / 2)).to_int16()

    def cmap(self, cmap: ColorMap):
        return dataclasses.replace(self, _cmap=cmap)

    def change_type(self, dtype: DataType):
        return self.local(lambda data: np.asanyarray(data, dtype=dtype))

    def to_int8(self):
        return self.round().change_type("int8")

    def to_int16(self):
        return self.round().change_type("int16")

    def to_int32(self):
        return self.round().change_type("int32")

    def to_int64(self):
        return self.round().change_type("int64")

    def save(self, file: str):
        with rasterio.open(
            file,
            "w",
            driver=driver_from_extension(file),
            height=self.height,
            width=self.width,
            count=1,
            crs=self.crs,
            transform=self.transform,
            dtype=self.data.dtype,
            nodata=self.nodata,
        ) as dataset:
            dataset.write(self.data, 1)


def read(file: str, band: int = 1):
    with rasterio.open(file) as dataset:
        data = dataset.read(band)

        if dataset.nodata is not None:
            data = np.where(data == dataset.nodata, np.nan, data)

        return Grid(
            data,
            dataset.crs,
            dataset.transform,
            dataset.nodata,
        )


def create(
    extent: Tuple[float, float, float, float],
    epsg: int,
    cell_size: float,
    value: Union[float, int],
):
    (xmin, ymin, xmax, ymax) = extent
    width = int(round((xmax - xmin) / cell_size))
    height = int(round((ymax - ymin) / cell_size))
    data = np.ones((height, width), int) * value
    crs = CRS.from_epsg(epsg)
    transform = from_bounds(xmin, ymin, xmax, ymax, width, height)
    return Grid(data, crs, transform, None)


def con(grid: Grid, trueValue: Operand, falseValue: Operand):
    return grid.local(
        lambda data: np.where(data, grid._data(trueValue), grid._data(falseValue))
    )


# IPython support
ipython = IPython.get_ipython()  # type: ignore

if ipython:

    def html(grid: Grid):
        with BytesIO() as buffer:
            figure = pyplot.figure(frameon=False)
            axes = figure.add_axes((0, 0, 1, 1))
            axes.axis("off")
            pyplot.imshow(grid.data, cmap=grid._cmap)
            pyplot.savefig(buffer)
            pyplot.close(figure)
            image = b64encode(buffer.getvalue()).decode()
            return f'<div>{grid}</div><img src="data:image/png;base64, {image}" /><div>{grid.extent}</div>'

    # type: ignore
    formatter = ipython.display_formatter.formatters["text/html"]
    formatter.for_type(Grid, html)
    formatter.for_type(
        tuple,
        lambda grids: f"""
            <table>
                <tr style="text-align: left">
                    {"".join(f"<td>{html(grid)}</td>" for grid in grids)}
                </tr>
            </table>
        """
        if all(isinstance(grid, Grid) for grid in grids)
        else f"{grids}",
    )
