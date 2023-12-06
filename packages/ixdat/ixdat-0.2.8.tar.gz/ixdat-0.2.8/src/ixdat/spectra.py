"""Base classes for spectra and spectrum series


Note on grammar:
----------------
The spectrum class corresponds to a database table which we call "spectrums". This
is an intentional misspelling of the plural of "spectrum". The correctly spelled
plural, "spectra", is reserved for a Field wrapping a 2-D array, each row of which
is the y values of a spectrum. This use of two plurals of "spectrum" is analogous
to the use of "persons" and "people" as distinct plurals of the word "person". While
"persons" implies that each person referred to should be considered individually,
"people" can be considered as a group.
"""

import numpy as np
from .db import Saveable, fill_object_list, PlaceHolderObject
from .data_series import DataSeries, TimeSeries, Field
from .exceptions import BuildError
from .plotters.spectrum_plotter import SpectrumPlotter, SpectrumSeriesPlotter
from .measurements import Measurement, get_combined_technique


class Spectrum(Saveable):
    """The Spectrum class.

    A spectrum is a data structure including one-dimensional arrays of x and y variables
    of equal length. Typically, information about the state of a sample can be obtained
    from a plot of y (e.g. absorbtion OR intensity OR counts) vs x (e.g energy OR
    wavelength OR angle OR mass-to-charge ratio). Even though in reality it takes time
    to require a spectrum, a spectrum is considered to represent one instance in time.

    In ixdat, the data of a spectrum is organized into a 1-Dimensional Field, where the
    y-data is considered to span a space defined by the x-data.

    The Spectrum class makes the data in this field intuitively available. If spec
    is a spectrum, spec.x and spec.y give access to the x and y data, respectively,
    while spec.xseries and spec.yseries give the corresponding DataSeries.
    """

    table_name = "spectrums"  # The misspelling is intentional. See :module:`~spectra`
    column_attrs = {
        "name",
        "technique",
        "metadata",
        "tstamp",
        "sample_name",
        "field_id",
    }
    child_attrs = ["fields"]

    def __init__(
        self,
        *,
        name,
        technique="spectrum",
        metadata=None,
        sample_name=None,
        reader=None,
        tstamp=None,
        field=None,
        field_id=None,
    ):
        """Initiate a spectrum

        Args:
            name (str): The name of the spectrum
            metadata (dict): Free-form spectrum metadata. Must be json-compatible.
            technique (str): The spectrum technique
            sample_name (str): The sample name
            reader (Reader): The reader, if read from file
            tstamp (float): The unix epoch timestamp of the spectrum
            field (Field): The Field containing the data (x, y, and tstamp)
            field_id (id): The id in the data_series table of the Field with the data,
                if the field is not yet loaded from backend.
        """
        super().__init__()
        self.name = name
        self.technique = technique
        self.metadata = metadata
        self.tstamp = tstamp
        self.sample_name = sample_name
        self.reader = reader
        # Note: the PlaceHolderObject can be initiated without the backend because
        #     if field_id is provided, then the relevant backend is the active one,
        #     which PlaceHolderObject uses by default.
        self._field = field or PlaceHolderObject(field_id, cls=Field)

        self.plotter = SpectrumPlotter(spectrum=self)
        # defining this method here gets it the right docstrings :D
        self.plot = self.plotter.plot

    @classmethod
    def read(cls, path_to_file, reader, **kwargs):
        """Return a Measurement object from parsing a file with the specified reader

        Args:
            path_to_file (Path or str): The path to the file to read
            reader (str or Reader class): The (name of the) reader to read the file with.
            kwargs: key-word arguments are passed on to the reader's read() method.
        """
        if isinstance(reader, str):
            # TODO: see if there isn't a way to put the import at the top of the module.
            #    see: https://github.com/ixdat/ixdat/pull/1#discussion_r546437471
            from .readers import READER_CLASSES

            reader = READER_CLASSES[reader]()
        # print(f"{__name__}. cls={cls}")  # debugging
        return reader.read(path_to_file, cls=cls, **kwargs)

    @classmethod
    def read_set(
        cls,
        path_to_file_start=None,
        part=None,
        suffix=None,
        file_list=None,
        reader=None,
        **kwargs,
    ):
        """Read and append a set of spectra as a SpectrumSeries

        Args:
            path_to_file_start (Path or str): The path to the files to read including
                the shared start of the file name: `Path(path_to_file).parent` is
                interpreted as the folder where the file are.
                `Path(path_to_file).name` is interpreted as the shared start of the files
                to be appended.
            part (Path or str): A path where the folder is the folder containing data
                and the name is a part of the name of each of the files to be read and
                combined.
            suffix (str): If a suffix is given, only files with the specified ending are
                added to the file list
            file_list (list of Path): As an alternative to path_to_file_start or part,
                the exact files to append can be specified in a list
            reader (str or Reader class): The (name of the) reader to read the files with
            kwargs: Key-word arguments are passed via cls.read() to the reader's read()
                method, AND to cls.from_component_measurements()
        """
        from .readers.reading_tools import get_file_list

        file_list = file_list or get_file_list(path_to_file_start, part, suffix)
        spectrum_list = [cls.read(f, reader=reader, **kwargs) for f in file_list]
        return SpectrumSeries.from_spectrum_list(spectrum_list)

    @property
    def data_objects(self):
        """The data-containing objects that need to be saved when the spectrum is saved.

        For a field to be correctly saved and loaded, its axes_series must be saved
        first. So there are three series in the data_objects to return
        FIXME: with backend-specifying id's, field could check for itself whether
        FIXME:  its axes_series are already in the database.
        """
        return self.series_list

    @classmethod
    def from_data(
        cls,
        x,
        y,
        tstamp=None,
        x_name="x",
        y_name="y",
        x_unit_name=None,
        y_unit_name=None,
        **kwargs,
    ):
        """Initiate a spectrum from data. Does so via cls.from_series

        Args:
            x (np array): x data
            y (np array): y data
            tstamp (timestamp): The timestamp of the spectrum. Defaults to None.
            x_name (str): Name of the x variable. Defaults to 'x'
            y_name (str): Name of the y variable. Defaults to 'y'
            x_unit_name (str): Name of the x unit. Defaults to None
            y_unit_name (str): Name of the y unit. Defaults to None
            kwargs: Key-word arguments are passed on ultimately to cls.__init__
        """
        xseries = DataSeries(data=x, name=x_name, unit_name=x_unit_name)
        yseries = DataSeries(data=y, name=y_name, unit_name=y_unit_name)
        return cls.from_series(xseries, yseries, tstamp, **kwargs)

    @classmethod
    def from_series(cls, xseries, yseries, tstamp, **kwargs):
        """Initiate a spectrum from data. Does so via cls.from_field

        Args:
            xseries (DataSeries): A series with the x data
            yseries (DataSeries): A series with the y data. The y data should be a
                vector of the same length as the x data.
            tstamp (timestamp): The timestamp of the spectrum. Defaults to None.
            kwargs: Key-word arguments are passed on ultimately to cls.__init__
        """
        field = Field(
            data=yseries.data,
            axes_series=[xseries],
            name=yseries.name,
            unit_name=yseries.unit_name,
        )
        kwargs.update(tstamp=tstamp)
        return cls.from_field(field, **kwargs)

    @classmethod
    def from_field(cls, field, **kwargs):
        """Initiate a spectrum from data. Does so via cls.from_field

        Args:
            field (Field): The field containing all the data of the spectrum.
                field.data is the y-data, which is considered to span x and t.
                field.axes_series[0] is a DataSeries with the x data.
                field.axes_series[1] is a TimeSeries with one time point.
            kwargs: key-word arguments are passed on ultimately to cls.__init__
        """
        spectrum_as_dict = kwargs
        spectrum_as_dict["field"] = field
        if "name" not in spectrum_as_dict:
            spectrum_as_dict["name"] = field.name
        return cls.from_dict(spectrum_as_dict)

    @property
    def field(self):
        """Since a spectrum can be loaded lazily, we make sure the field is loaded"""
        if isinstance(self._field, PlaceHolderObject):
            self._field = self._field.get_object()
        return self._field

    @property
    def fields(self):
        return [self.field]

    @property
    def field_id(self):
        """The id of the field"""
        return self.field.id

    @property
    def xseries(self):
        """The x DataSeries is the first axis of the field"""
        return self.field.axes_series[0]

    @property
    def series_list(self):
        """A Spectrum's series list includes its field and its axes_series."""
        return [self.field] + self.field.axes_series

    @property
    def x(self):
        """The x data is the data attribute of the xseries"""
        return self.xseries.data

    @property
    def x_name(self):
        """The name of the x variable is the name attribute of the xseries"""
        return self.xseries.name

    @property
    def yseries(self):
        """The yseries is a DataSeries reduction of the field"""
        return DataSeries(
            name=self.field.name, data=self.y, unit_name=self.field.unit_name
        )

    @property
    def y(self):
        """The y data is the one-dimensional data attribute of the field"""
        return self.field.data

    @property
    def y_name(self):
        """The name of the y variable is the name attribute of the field"""
        return self.field.name

    @property
    def tseries(self):
        """The TimeSeries of a spectrum is a single point [0] and its tstamp"""
        return TimeSeries(
            name="time / [s]", unit_name="s", data=np.array([0]), tstamp=self.tstamp
        )

    def __add__(self, other):
        """Adding spectra makes a (2)x(N_x) SpectrumSeries. self comes before other."""
        if not self.x == other.x:  # FIXME: Some depreciation here. How else?
            raise BuildError(
                "can't add spectra with different `x`. "
                # "Consider the function `append_spectra` instead."
            )
        t = np.array([0, other.tstamp - self.tstamp])
        tseries = TimeSeries(
            name="time / [s]", unit_name="s", data=t, tstamp=self.tstamp
        )
        new_field = Field(
            name=self.name,
            unit_name=self.field.unit_name,
            data=np.array([self.y, other.y]),
            axes_series=[tseries, self.xseries],
        )
        spectrum_series_as_dict = self.as_dict()
        technique = self.technique
        if technique.endswith("spectrum"):
            technique = technique.rstrip("spectrum") + "spectra"
        spectrum_series_as_dict.update(technique=technique)
        spectrum_series_as_dict["field"] = new_field
        del spectrum_series_as_dict["field_id"]

        return SpectrumSeries.from_dict(spectrum_series_as_dict)


class MultiSpectrum(Saveable):
    """The MultiSpectrum class.

    A collection of spectra having the same x values and tstamp. The y values of the
    spectra in a MultiSpectrum can describe the same kind of thing, such as in the
    multiple scans of an XPS measurement, where the average of the spectra is the
    most-used quantity; or can different things, like fluorescence and transmission
    measured simultaneously while varying the incident x-ray energy on a beamline.

    Indexing with a spectrum name returns a `Spectrum` object with that thing, or a
    smaller `MultiSpectrum` if there are multiple spectra with that name.
    """

    table_name = "multispectrum"
    column_attrs = {
        "name",
        "technique",
        "metadata",
        "tstamp",
        "sample_name",
    }
    extra_linkers = {"multispectrum_fields": {"data_series", "field_ids"}}
    child_attrs = ["fields"]

    def __init__(
        self,
        *,
        name,
        technique=None,
        tstamp=None,
        sample_name=None,
        metadata=None,
        fields=None,
        field_ids=None,
    ):
        """Initiate a multi-spectrum

        Args:
            name (str): The name of the multi-spectrum
            technique (str): The spectrum technique
            tstamp (float): The unix epoch timestamp of the spectrum
            sample_name (str): The sample name
            metadata (dict): Free-form spectrum metadata. Must be json-compatible.
            fields (list of Field): The Fields containing the data (x, y)
            field_ids (list of int): The id's of Fields if available from the backend.
        """
        super().__init__()
        self.name = name
        self.technique = technique
        self.metadata = metadata
        self.tstamp = tstamp
        self.sample_name = sample_name
        self._fields = fill_object_list(object_list=fields, obj_ids=field_ids, cls=Field)
        self._xseries = None
        self._spectrum_list = None

    @property
    def fields(self):
        """Make sure Fields are loaded and have the same xseries"""
        xseries = None  # Enter the loop without an x series
        for i, f in enumerate(self._fields):
            if isinstance(f, PlaceHolderObject):
                # load or "unpack" any fields for which only the id's were loaded:
                self._fields[i] = f.get_object()
            if i > 0:
                # If all the xseries are the same, every field after the first should
                # have an equivalent xseries to that of the previous field:
                assert self._fields[i].axes_series[0] == xseries
            # use the xseries of this field for comparison with the xseries of the next:
            xseries = self._fields[i].axes_series[0]
        # Now we've loaded any place-holder fields and checked their xseries are equal.
        return self._fields

    @property
    def xseries(self):
        """The shared xseries of all the spectra in the multi-spectrum"""
        if not self._xseries:
            self._xseries = self._fields[0].axes_series[0]
        return self._xseries

    @property
    def spectrum_list(self):
        """The spectra of the multi-spectrum as a list of Spectrum objects."""
        if not self._spectrum_list:
            self._spectrum_list = []
            for field in self.fields:
                s = Spectrum.from_field(
                    field,
                    name=field.name,
                    technique=self.technique,
                    metadata=self.metadata,
                    tstamp=self.tstamp,
                    sample_name=self.sample_name,
                )
                self._spectrum_list.append(s)
        return self._spectrum_list

    def __getitem__(self, name):
        """Indexing a MultiSpectrum returns the spectrum with the requested name."""
        spectrum_list = [s for s in self.spectrum_list if s.name == name]
        if len(spectrum_list) == 1:
            return spectrum_list[0]
        elif len(spectrum_list) > 1:
            return self.__class__.from_spectrum_list(
                spectrum_list,
                technique=self.technique,
                metadata=self.metadata,
            )

    @classmethod
    def from_spectrum_list(
        cls, spectrum_list, technique=None, metadata=None, sample_name=None
    ):
        """Build a SpectrumSeries from a list of Spectrums"""
        fields = [spectrum.field for spectrum in spectrum_list]
        tstamp = spectrum_list[0].tstamp
        technique = spectrum_list[0].technique
        if technique.endswith("spectrum"):
            technique = technique.rstrip("spectrum") + "spectra"
        obj_as_dict = {
            "fields": fields,
            "technique": technique,
            "metadata": metadata,
            "tstamp": tstamp,
            "sample_name": sample_name,
        }
        return cls.from_dict(obj_as_dict)


class SpectrumSeries(Spectrum):
    """The SpectrumSeries class.

    A spectrum series is a data structure including a two-dimensional array, each row of
    which is a spectrum, and each column of which is one spot in the spectrum as it
    changes with some other variable.

    In ixdat, the data of a spectrum series is organized into a Field, where the y-data
    is considered to span a space defined by a DataSeries which is the x data, and a
    DataSeries (typically a TimeSeries) which enumerates or specifies when or under
    which conditions each spectrum was taken. The spectrum series will consider this
    its "time" variable even if it is not actually time.

    The SpectrumSeries class makes the data in this field intuitively available. If
    spec is a spectrum series, spec.x is the x data with shape (N, ), spec.t is the
    time data with shape (M, ), and spec.y is the spectrum data with shape (M, N).
    """

    def __init__(self, *args, **kwargs):
        """Initiate a spectrum series

        Args:
            name (str): The name of the spectrum series
            metadata (dict): Free-form spectrum metadata. Must be json-compatible.
            technique (str): The spectrum technique
            sample_name (str): The sample name
            reader (Reader): The reader, if read from file
            tstamp (float): The unix epoch timestamp of the spectrum
            field (Field): The Field containing the data (x, y, and tstamp)
            field_id (id): The id in the data_series table of the Field with the data,
                if the field is not yet loaded from backend.
        """
        if "technique" not in kwargs:
            kwargs["technique"] = "spectra"
        super().__init__(*args, **kwargs)
        self.plotter = SpectrumSeriesPlotter(spectrum_series=self)
        self.heat_plot = self.plotter.heat_plot

    @classmethod
    def from_spectrum_list(cls, spectrum_list, **kwargs):
        """Build a SpectrumSeries from a list of Spectrum objects."""
        xseries = None
        tstamp_list = []
        ys = []
        technique = spectrum_list[0].technique

        for spectrum in spectrum_list:
            tstamp_list.append(spectrum.tstamp)
            xseries = xseries or spectrum.xseries
            ys.append(spectrum.y)

        tseries = TimeSeries(
            name="Spectrum Time",
            unit_name="s",
            data=np.array(tstamp_list) - tstamp_list[0],
            tstamp=tstamp_list[0],
        )
        field = Field(
            name=spectrum_list[0].field.name,
            unit_name=spectrum_list[0].field.unit_name,
            axes_series=[tseries, xseries],
            data=np.stack(ys),
        )
        if technique.endswith("spectrum"):
            technique = technique.rstrip("spectrum") + "spectra"

        obj_as_dict = spectrum_list[0].as_dict()
        obj_as_dict["field"] = field
        obj_as_dict["technique"] = technique
        del obj_as_dict["field_id"]
        obj_as_dict.update(kwargs)
        return cls.from_dict(obj_as_dict)

    @property
    def yseries(self):
        # Should this return an average or would that be counterintuitive?
        raise BuildError(
            f"{self} has no single y-series. Index it to get a Spectrum "
            "or see `y_average`"
        )

    @property
    def tseries(self):
        """The TimeSeries of a SectrumSeries is the 0'th axis of its field.
        Note that its data is not sorted!
        """
        return self.field.axes_series[0]

    @property
    def t(self):
        """The time array of a SectrumSeries is the data of its tseries.
        Note that it it is not sorted!
        """
        return self.tseries.data

    @property
    def t_name(self):
        """The name of the time variable of the spectrum series"""
        return self.tseries.name

    @property
    def xseries(self):
        """The x-axis DataSeries of a SectrumSeries is the 1'st axis of its field"""
        return self.field.axes_series[1]

    @property
    def x(self):
        """The x (scanning variable) data"""
        return self.xseries.data

    @property
    def x_name(self):
        """The name of the scanning variable"""
        return self.xseries.name

    @property
    def y(self):
        """The y data is the multi-dimensional data attribute of the field"""
        return self.field.data

    def __getitem__(self, key):
        """Indexing a SpectrumSeries with an int n returns its n'th spectrum"""
        if isinstance(key, int):
            spectrum_as_dict = self.as_dict()
            del spectrum_as_dict["field_id"]
            spectrum_as_dict["field"] = Field(
                # note that it's important in some cases that the spectrum does not have
                # the same name as the spectrum series:
                name=self.y_name + "_" + str(key),
                unit_name=self.field.unit_name,
                data=self.y[key],
                axes_series=[self.xseries],
            )
            spectrum_as_dict["tstamp"] = self.tstamp + self.t[key]
            return Spectrum.from_dict(spectrum_as_dict)
        raise KeyError

    @property
    def y_average(self):
        """The y-data of the average spectrum"""
        return np.mean(self.y, axis=0)

    def __add__(self, other):
        if isinstance(other, Measurement):
            return add_spectrum_series_to_measurement(other, self)
        raise NotImplementedError("Appending `SpectrumSeries` is not yet implemented")


def add_spectrum_series_to_measurement(measurement, spectrum_series, **kwargs):
    """Add a measurement and a spectrum measurement.

    Args:
        measurement (Measurement): The `Measurement` object containing the time-resolved
            scalar values.
        spectrum_series (SpectrumSeries): The `SpectrumSeries` object containing the 2-D
            time-resolved spectral data.
        kwargs: Additional key-word arguments are passed on to the `from_dict`
            constructor of the resulting object.

    Returns SpectroMeasurement: The addition results in an object of SpectroMeasurement
        or a subclass thereof if ixdat supports the hyphenated technique. For example,
        addition of an `ECMeasurement` and an XAS `SpectrumSeries` results in an
        `ECXASMeasurement` object.
    """
    new_name = measurement.name + " AND " + spectrum_series.name
    new_technique = get_combined_technique(
        measurement.technique, spectrum_series.technique
    )

    # TODO: see if there isn't a way to put the import at the top of the module.
    #    see: https://github.com/ixdat/ixdat/pull/1#discussion_r546437410
    from .techniques import TECHNIQUE_CLASSES

    obj_as_dict = measurement.as_dict()
    obj_as_dict["spectrum_series"] = spectrum_series
    obj_as_dict["name"] = new_name
    obj_as_dict["technique"] = new_technique

    if new_technique in TECHNIQUE_CLASSES:
        cls = TECHNIQUE_CLASSES[new_technique]
    else:
        cls = SpectroMeasurement
    if issubclass(cls, TECHNIQUE_CLASSES["EC-Optical"]):
        # Then we need a reference spectrum!
        # But so far the only EC-Optical reader doesn't support reading Optical and
        # EC parts separately, so this needs not be implemented yet.
        raise NotImplementedError("addition of EC and Optical not yet supported.")

    obj_as_dict.update(kwargs)
    return cls.from_dict(obj_as_dict)


class SpectroMeasurement(Measurement):
    extra_column_attrs = {"spectro_measurements": {"spectrum_id"}}

    def __init__(self, *args, spectrum_series=None, spec_id=None, **kwargs):
        super().__init__(*args, **kwargs)
        if spectrum_series:
            self._spectrum_series = spectrum_series
        elif spec_id:
            self._spectrum_series = PlaceHolderObject(spec_id, cls=SpectrumSeries)
        else:
            raise TypeError(
                "A SpectroMeasurement must be "
                "initialized with a `spectrum_series` or `spectrum_id`"
            )

    @property
    def spectrum_series(self):
        """The `SpectrumSeries` with the spectral data"""
        if isinstance(self._spectrum_series, PlaceHolderObject):
            self._spectrum_series = self._spectrum_series.get_object()
        return self._spectrum_series

    @property
    def spectrum_id(self):
        """The id of the `SpectrumSeries`"""
        return self.spectrum_series.id

    @property
    def spectra(self):
        """The field of the `SpectrumSeries`. `spectra.data` is a 2-D array"""
        return self.spectrum_series.field

    def set_spectrum_series(self, spectrum_series):
        """(Re-)set the `spectrum_series` to a provided `spectrum_series`"""
        self._spectrum_series = spectrum_series

    def __add__(self, other):
        added_measurement = super().__add__(other)
        if isinstance(other, SpectroMeasurement):
            spectrum_series = self.spectrum_series + other.spectrum_series
            added_measurement.set_spectrum_series(spectrum_series)
        return added_measurement

    def cut(self, tspan, t_zero=None):
        """Select the portion of the data in a given tspan.

        See :func:`~measurements.Measurement.cut`
        """
        cut_measurement = super().cut(tspan, t_zero=t_zero)
        spectrum_series = self.spectrum_series.cut(tspan=tspan)
        cut_measurement.set_spectrum_series(spectrum_series)
        return cut_measurement
