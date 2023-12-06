"""Import readers and build the READER_CLASSES dictionary for direct import

Constants:
    READER_CLASSES (dict): Dictionary of {reader_name: ReaderClass} where
        reader_name is the name of the backend (like "directory") and ReaderClass
        is the reader class for parsing files.
"""
from ..techniques import TECHNIQUE_CLASSES

# ixdat
from .ixdat_csv import IxdatCSVReader, IxdatSpectrumReader

# potentiostats
from .biologic import BiologicMPTReader
from .autolab import NovaASCIIReader
from .ivium import IviumDatasetReader
from .chi import CHInstrumentsTXTReader

# mass spectrometers
from .pfeiffer import PVMassSpecReader
from .rgasoft import StanfordRGASoftReader
from .cinfdata import CinfdataTXTReader
from .cinfdata_db import CinfdataDBReader

# ec-ms
from .zilien import ZilienTSVReader, ZilienTMPReader, ZilienSpectrumReader
from .ec_ms_pkl import EC_MS_CONVERTER

# spectroelectrochemistry
from .msrh_sec import MsrhSECReader, MsrhSECDecayReader

# xrd
from .xrdml import XRDMLReader

# xps
from .avantage import AvantageAVGReader

# xas
from .qexafs import QexafsDATReader

READER_CLASSES = {
    "ixdat": IxdatCSVReader,
    "ixdat_spectrum": IxdatSpectrumReader,
    "biologic": BiologicMPTReader,
    "avantage": AvantageAVGReader,
    "autolab": NovaASCIIReader,
    "ivium": IviumDatasetReader,
    "chi": CHInstrumentsTXTReader,
    "pfeiffer": PVMassSpecReader,
    "rgasoft": StanfordRGASoftReader,
    "cinfdata": CinfdataTXTReader,
    "cinfdata_db": CinfdataDBReader,
    "zilien": ZilienTSVReader,
    "zilien_tmp": ZilienTMPReader,
    "zilien_spec": ZilienSpectrumReader,
    "EC_MS": EC_MS_CONVERTER,
    "msrh_sec": MsrhSECReader,
    "msrh_sec_decay": MsrhSECDecayReader,
    "xrdml": XRDMLReader,
    "qexafs": QexafsDATReader,
}
