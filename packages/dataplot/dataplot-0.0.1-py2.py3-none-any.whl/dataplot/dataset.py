"""
Contains the dataset interface: PlotData.

NOTE: this module is private. All functions and objects are available in the main
`dataplot` namespace - use that instead.

"""
from abc import ABCMeta
from functools import partial
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Iterable,
    List,
    Optional,
    TypeVar,
    Union,
    overload,
)

import numpy as np
import pandas as pd
from hintwith import hintwith
from typing_extensions import Self

from .histogram import Histogram
from .linechart import LineChart
from .setter import FigWrapper, PlotSetter, PlotSettings

if TYPE_CHECKING:
    from numpy.typing import NDArray


T = TypeVar("T")

__all__ = ["PlotData"]


class PlotData(PlotSetter, metaclass=ABCMeta):
    """
    Provides methods for mathematical operations and plotting.

    """

    @overload
    def __new__(cls, data: "NDArray", label: Optional[str] = None) -> "PlotData":
        ...

    @overload
    def __new__(
        cls, data: List["NDArray"], label: Optional[List[str]] = None
    ) -> "PlotData":
        ...

    def __new__(
        cls,
        data: Union["NDArray", List["NDArray"]],
        label: Union[str, List[str], None] = None,
    ) -> "PlotData":
        """
        Initializes a dataset interface which provides methods for mathematical
        operations and plotting.

        Parameters
        ----------
        data : Union[NDArray, List[NDArray]]
            Input values, this takes either a single array or a list of arrays, each
            representing a set of data.
        label : Union[str, List[str], None], optional
            Labels of the data, this takes either a single string or a list of strings.
            If is a list, should be the same length as `data`, with each element
            corresponding to a specific array in `data`. By default None.

        Returns
        -------
        PlotData
            Provides methods for mathematical operations and plotting.

        """
        if isinstance(data, list):
            if label is None:
                label = cls.__default_label(len(data))
            dataset: List["PlotData"] = [PlotData(d, lb) for d, lb in zip(data, label)]
            return _PlotDataBatch(*dataset)
        return cls.__base__.__new__(cls)

    def __init__(self, data: "NDArray", label: Optional[str] = None) -> None:
        self.data = data
        self.label = self.__default_label(1)[0] if label is None else label
        self.fmt: str = "{0}"
        self.fmtdata = self.data
        self.settings = PlotSettings()

    @classmethod
    def __subclasshook__(cls, __subclass: type) -> bool:
        """
        Checks if a given subclass is a subclass of `PlotData`.

        Parameters
        ----------
        __subclass : type
            The class that is being checked.

        Returns
        -------
        bool
            Returns whether the given subclass is a subclass of `PlotData`.

        """
        if issubclass(__subclass, _PlotDataBatch):
            return True
        return super().__subclasshook__(__subclass)

    @classmethod
    def __default_label(cls, n: int = 1) -> List[str]:
        """
        Generates default labels for the data.

        Parameters
        ----------
        n : int, optional
            Number of labels, by default 1.

        Returns
        -------
        List[str]
            List of labels.

        """
        return [f"x{i}" for i in range(1, 1 + n)]

    def __create(self, fmt: str, fmtdata: "NDArray") -> "PlotData":
        obj = self.customize(self.__class__, self.data, self.label)
        obj.fmt = fmt
        obj.fmtdata = fmtdata
        return obj

    def set_label(self, label: Union[str, List[str], None] = None) -> Self:
        """
        Reset the labels.

        Parameters
        ----------
        label : Union[str, List[str], None], optional
            Labels of the data, this takes either a single string or a list of strings.
            If is a list, should be the same length as `data`, with each element
            corresponding to a specific array in `data`. By default None.

        Returns
        -------
        Self
            An instance of self.

        """
        if label is not None:
            self.label = label
            self.fmt = "{0}"
        return self

    @property
    def fmtlabel(self) -> str:
        """
        Returns the formatted label.

        Returns
        -------
        str
            Formatted label.

        """
        return self.fmt.format(self.label)

    def join(self, *others: "PlotData") -> "PlotData":
        """
        Merge two or more `PlotData` instances, integrating the attributes
        of each.

        Parameters
        ----------
        *others : PlotData
            The instances to be merged.

        Returns
        -------
        PlotData
            A new instance of `PlotData`.

        """
        return _PlotDataBatch(self, *others)

    def log(self) -> "PlotData":
        """
        Perform a log operation on the data.

        Returns
        -------
        PlotData
            A new instance of `PlotData`.

        """
        new_fmt = f"log({self.fmt})"
        new_fmtdata = np.log(self.fmtdata)
        return self.__create(new_fmt, new_fmtdata)

    def rolling(self, n: int) -> "PlotData":
        """
        Perform a rolling-mean operation on the data.

        Parameters
        ----------
        n : int
            Specifies the window size for calculating the rolling average of
            the data points.

        Returns
        -------
        PlotData
            A new instance of `PlotData`.

        """
        new_fmt = f"rolling({self.fmt}, {n})"
        new_fmtdata = pd.Series(self.fmtdata).rolling(n).mean().values
        return self.__create(new_fmt, new_fmtdata)

    def exp(self) -> "PlotData":
        """
        Perform an exp operation on the data.

        Returns
        -------
        PlotData
            A new instance of `PlotData`.

        """
        new_fmt = f"exp({self.fmt})"
        new_fmtdata = np.exp(self.fmtdata)
        return self.__create(new_fmt, new_fmtdata)

    def demean(self) -> "PlotData":
        """
        Perform a demean operation on the data by subtracting its mean.

        Returns
        -------
        PlotData
            A new instance of `PlotData`.

        """
        new_fmt = f"{self.fmt} - mean({self.fmt})"
        new_fmtdata = self.fmtdata - np.nanmean(self.fmtdata)
        return self.__create(new_fmt, new_fmtdata)

    def zscore(self) -> "PlotData":
        """
        Perform a zscore operation on the data by subtracting its mean and then
        dividing by its standard deviation.

        Returns
        -------
        PlotData
            A new instance of `PlotData`.

        """
        new_fmt = f"({self.fmt} - mean({self.fmt})) / std({self.fmt})"
        new_fmtdata = (self.fmtdata - np.nanmean(self.fmtdata)) / np.nanstd(
            self.fmtdata
        )
        return self.__create(new_fmt, new_fmtdata)

    def cumsum(self) -> "PlotData":
        """
        Perform a cumsum operation on the data by calculating its cummulative
        sums.

        Returns
        -------
        PlotData
            A new instance of `PlotData`.

        """
        new_fmt = f"cumsum({self.fmt})"
        new_fmtdata = np.cumsum(self.fmtdata)
        return self.__create(new_fmt, new_fmtdata)

    def reset(self) -> Self:
        """
        Reset all the operations.

        Returns
        -------
        Self
            An instance of self.
        """
        self.fmt = "{0}"
        self.fmtdata = self.data
        return self

    @hintwith(Histogram.__init__)
    def hist(self, **kwargs) -> None:
        """
        Plot a histogram of the data.

        Parameters
        ----------
        bins : int, optional
            Specifies the number of bins to divide the data into for the histogram
            plot, by default 100.
        fit : bool, optional
            Fit a curve to the histogram or not, by default True.
        density : bool, optional
            Draw a probability density or not. If True, the histogram will be
            normalized such that the area under it equals to 1. By default True.
        same_bin : bool, optional
            Determines whether the bins should be the same for all sets of data, by
            default True.
        stats : bool, optional
            Determines whether to show the statistics, including the calculated mean,
            standard deviation, skewness, and kurtosis of the input, by default True.
        on : Optional[AxesWrapper], optional
            Specifies the axes wrapper on which the histogram should be plotted. If
            not specified, the histogram will be plotted on a new axes in a new
            figure. By default None.

        """
        with unbatched(self.customize)(FigWrapper, 1, 1) as fig:
            kwargs["on"] = fig.axes[0]
            self.customize(
                Histogram,
                data=self.fmtdata,
                label=self.fmtlabel,
                **kwargs,
            ).perform()

    @hintwith(LineChart.__init__)
    def plot(self, **kwargs) -> None:
        """
        Create a line chart for the data.

        Parameters
        ----------
        scatter : bool, optional
            Determines whether to include scatter points in the line chart, by default
            False.
        figsize_adjust : bool, optional
            Determines whether the size of the figure should be adjusted automatically
            based on the data being plotted, by default True.
        on : Optional[AxesWrapper], optional
            Specifies the axes wrapper on which the line chart should be plotted. If
            not specified, the histogram will be plotted on a new axes in a new
            figure. By default None.

        """
        with unbatched(self.customize)(FigWrapper, 1, 1) as fig:
            kwargs["on"] = fig.axes[0]
            self.customize(
                LineChart,
                data=self.fmtdata,
                label=self.fmtlabel,
                **kwargs,
            ).perform()


class _PlotDataBatch:
    def __init__(self, *args: Any) -> None:
        if not args:
            raise ValueError("number of data sets is 0")
        self.children: List[PlotData] = []
        for a in args:
            if isinstance(a, self.__class__):
                self.children.extend(a.children)
            else:
                self.children.append(a)

    def __getattr__(self, __name: str) -> Any:
        if __name in {"hist", "plot", "set_label"}:
            return partial(getattr(PlotData, __name), self)
        attribs = (getattr(c, __name) for c in self.children)
        if __name in {"set_plot", "set_plot_default"}:
            return BatchList(attribs, returns=self)
        if __name == "customize":
            return BatchList(attribs, reflex="reflex")
        return BatchList(attribs, reducer=lambda x: self.__class__(*x))

    def __setattr__(self, __name: str, __value: Any) -> None:
        if __name in {"fmt", "label"}:
            attribs = (partial(c.__setattr__, __name) for c in self.children)
            BatchList(attribs)(batched(__value))
        else:
            super().__setattr__(__name, __value)


class BatchList(list):
    """
    A subclass of `list` that enables batched attrubutes-getting and calling.
    Differences to `list` that if the `__getattr__()` or `__call__()` method
    is called, each element's `__getattr__()` or `__call__()` will be called
    instead, and the results come as a new `BatchList` object.

    Parameters
    ----------
    *args : Any
        Arguments for initializing a `list` object.
    returns : Any, optional
        Specifies the returns of `__call__()`. If not specified, a new
        `BatchList` object will be returned. By default None.
    reducer : Optional[Callable], optional
        Specifies a reducer for the returns of `__call__()`, by default None.
    reflex : Optional[str], optional
        If str, the returns of an element's `__call__()` will be provided to
        the next element as a keyword argument named as `reflex`, by default
        None.

    """

    @overload
    def __init__(
        self,
        returns: Any = None,
        reducer: Optional[Callable] = None,
        reflex: Optional[str] = None,
    ) -> None:
        ...

    @overload
    def __init__(
        self,
        __iterable: Iterable,
        /,
        returns: Any = None,
        reducer: Optional[Callable] = None,
        reflex: Optional[str] = None,
    ) -> None:
        ...

    def __init__(
        self,
        *args: Any,
        returns: Any = None,
        reducer: Optional[Callable] = None,
        reflex: Optional[str] = None,
    ) -> None:
        self.__returns = returns
        self.__reducer = reducer
        self.__reflex = reflex
        super().__init__(*args)

    def __getattr__(self, __name: str):
        return BatchList(
            (getattr(x, __name) for x in self),
            returns=self.__returns,
            reducer=self.__reducer,
            reflex=self.__reflex,
        )

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        batch: BatchList = self.__class__([], reflex=self.__reflex)
        for i, obj in enumerate(self):
            clean_args = [a[i] if isinstance(a, self.__class__) else a for a in args]
            clean_kwargs = {
                k: v[i] if isinstance(v, self.__class__) else v
                for k, v in kwargs.items()
            }
            if self.__reflex and i > 0:
                clean_kwargs[self.__reflex] = r
            batch.append(r := obj(*clean_args, **clean_kwargs))
        returns = batch if self.__returns is None else self.__returns
        return self.__reducer(returns) if self.__reducer is not None else returns


def batched(x: T) -> T:
    """
    If a `list` object is provided, returns a `BatchList` object initialized
    by it. Otherwise, return the input itself.

    Parameters
    ----------
    x : T
        Can be a list or anything else.

    Returns
    -------
    T
        Batched object.

    """
    return BatchList(x) if isinstance(x, list) else x


def unbatched(x: T) -> T:
    """
    If a `BatchList` object is provided, returns its last element.
    Otherwise, return the input itself.

    Parameters
    ----------
    x : T
        Can be an instance of `BatchList` or anything else.

    Returns
    -------
    T
        Unbatched object.

    """
    return x[-1] if isinstance(x, BatchList) else x
