# midgard.parsers
Framework for parsers

**Description:**

To add a new parser, simply create a new .py-file which defines a class
inheriting from parsers.Parser. The class needs to be decorated with the
`midgard.dev.plugins.register` decorator as follows:

    from midgard.parsers import parser
    from midgard.lib import plugins

    @plugins.register
    class MyNewParser(parser.Parser):
        ...

To use a parser, you will typically use the `parse_file`-function defined below

    from midgard import parsers
    my_new_parser = parsers.parse_file('my_new_parser', 'file_name.txt', ...)
    my_data = my_new_parser.as_dict()

The name used in `parse_file` to call the parser is the name of the module
(file) containing the parser.


### **names**()

Full name: `midgard.parsers.names`

Signature: `() -> List[str]`

List the names of the available parsers

**Returns:**

Names of the available parsers


### **parse_file**()

Full name: `midgard.parsers.parse_file`

Signature: `(parser_name: str, file_path: Union[str, pathlib.Path], encoding: Optional[str] = None, timer_logger: Optional[Callable[[str], NoneType]] = None, use_cache: bool = False, **parser_args: Any) -> midgard.parsers._parser.Parser`

Use the given parser on a file and return parsed data

Specify `parser_name` and `file_path` to the file that should be parsed. The following parsers are available:

{doc_parser_names}

Data can be retrieved either as Dictionaries, Pandas DataFrames or Midgard Datasets by using one of the methods
`as_dict`, `as_dataframe` or `as_dataset`.

Example:

    >>> df = parse_file('rinex2_obs', 'ande3160.16o').as_dataframe()  # doctest: +SKIP

**Args:**

- `parser_name`:    Name of parser
- `file_path`:      Path to file that should be parsed.
- `encoding`:       Encoding in file that is parsed.
- `timer_logger`:   Logging function that will be used to log timing information.
- `use_cache`:      Whether to use a cache to avoid parsing the same file several times. (TODO: implement this)
- `parser_args`:    Input arguments to the parser

**Returns:**

- `Parser`:  Parser with the parsed data


## midgard.parsers._parser
Basic functionality for parsing datafiles, extended by individual parsers

**Description:**

This module contains functions and classes for parsing datafiles. It should typically be used by calling
`parsers.parse_file`:

**Example:**

    from midgard import parsers
    my_new_parser = parsers.parse_file('my_new_parser', 'file_name.txt', ...)
    my_data = my_new_parser.as_dict()



### **Parser**

Full name: `midgard.parsers._parser.Parser`

Signature: `(file_path: Union[str, pathlib.Path], encoding: Optional[str] = None) -> None`

An abstract base class that has basic methods for parsing a datafile

This class provides functionality for parsing a file. You should inherit from one of the specific parsers like for
instance ChainParser, LineParser, SinexParser etc

**Attributes:**

data (Dict):                  The (observation) data read from file.
data_available (Boolean):     Indicator of whether data are available.
file_encoding (String):       Encoding of the datafile.
file_path (Path):             Path to the datafile that will be read.
meta (Dict):                  Metainformation read from file.
parser_name (String):         Name of the parser (as needed to call parsers.parse_...).        


## midgard.parsers._parser_chain
Basic functionality for parsing datafiles line by line

**Description:**

This module contains functions and classes for parsing datafiles.


**Example:**

    from midgard import parsers
    my_new_parser = parsers.parse_file('my_new_parser', 'file_name.txt', ...)
    my_data = my_new_parser.as_dict()



### **ChainParser**

Full name: `midgard.parsers._parser_chain.ChainParser`

Signature: `(file_path: Union[str, pathlib.Path], encoding: Optional[str] = None) -> None`

An abstract base class that has basic methods for parsing a datafile

This class provides functionality for parsing a file with chained groups of information. You should inherit from
this one, and at least specify the necessary parameters in `setup_parser`.


### **ParserDef**

Full name: `midgard.parsers._parser_chain.ParserDef`

Signature: `(end_marker: Callable[[str, int, str], bool], label: Callable[[str, int], Any], parser_def: Dict[Any, Dict[str, Any]], skip_line: Optional[Callable[[str], bool]] = None, end_callback: Optional[Callable[[Dict[str, Any]], NoneType]] = None)`

A convenience class for defining the necessary fields of a parser

A single parser can read and parse one group of datalines, defined through the ParserDef by specifying how to parse
each line (parser_def), how to identify each line (label), how to recognize the end of the group of lines
(end_marker) and finally what (if anything) should be done after all lines in a group is read (end_callback).

The end_marker, label, skip_line and end_callback parameters should all be functions with the following signatures:

    end_marker   = func(line, line_num, next_line)
    label        = func(line, line_num)
    skip_line    = func(line)
    end_callback = func(cache)

The parser definition `parser_def` includes the `parser`, `field`, `strip` and `delimiter` entries. The `parser`
entry points to the parser function and the `field` entry defines how to separate the line in fields. The separated
fields are saved either in a dictionary or in a list. In the last case the line is split on whitespace by
default. With the `delimiter` entry the default definition can be overwritten, whereby also regular expressions can
be used (like '\s+' for remove whitespaces. Leading and trailing whitespace characters are removed by default 
before a line is parsed.  This default can be overwritten by defining the characters, which should be removed with 
the 'strip' entry. The `parser` dictionary is defined like:

    parser_def = { <label>: {'fields':    <dict or list of fields>,
                             'parser':    <parser function>,
                             'delimiter': <optional delimiter for splitting line>,
                             'strip':     <optional characters to be removed from beginning and end of line>
                 }}

**Args:**

- `end_marker`:   A function returning True for the last line in a group.
- `label`:        A function returning a label used in the parser_def.
- `parser_def`:   A dict with 'parser' and 'fields' defining the parser.
- `skip_line`:    A function returning True if the line should be skipped.
- `end_callback`: A function called after reading all lines in a group.


## midgard.parsers._parser_line
Basic functionality for parsing datafiles line by line using Numpy

**Description:**

This module contains functions and classes for parsing datafiles.


**Example:**

    from midgard import parsers
    my_new_parser = parsers.parse_file('my_new_parser', 'file_name.txt', ...)
    my_data = my_new_parser.as_dict()



### **LineParser**

Full name: `midgard.parsers._parser_line.LineParser`

Signature: `(file_path: Union[str, pathlib.Path], encoding: Optional[str] = None) -> None`

An abstract base class that has basic methods for parsing a datafile

This class provides functionality for using numpy to parse a file line by line. You should inherit from this one,
and at least specify the necessary parameters in `setup_parser`.


## midgard.parsers._parser_rinex
Basic functionality for parsing Rinex files

**Description:**

This module contains functions and classes for parsing Rinex files.

This file defines the general structure shared by most types of Rinex files, including header information. More
specific format details are implemented in subclasses. When calling the parser, you should call the apropriate parser
for a given Rinex format.



### **RinexHeader**

Full name: `midgard.parsers._parser_rinex.RinexHeader`

Signature: `(marker: str, fields: Dict[str, Tuple[int, int]], parser: Callable[[Dict[str, str]], Dict[str, Any]])`

A convenience class for defining how a Rinex header is parsed

**Args:**

- `marker`:  Marker of header (as defined in columns 60 and onward).
- `fields`:  Dictionary with field names as keys, tuple of start- and end-columns as value.
- `parser`:  Function that will parse the fields.


### **RinexParser**

Full name: `midgard.parsers._parser_rinex.RinexParser`

Signature: `(file_path: Union[str, pathlib.Path], encoding: Optional[str] = None, logger=<built-in function print>, sampling_rate: Optional[int] = None, strict: bool = False) -> None`

An abstract base class that has basic methods for parsing a datafile

This class provides functionality for reading Rinex header data. You should inherit from this one,
and at least implement `parse_epochs`.


### **parser_cache**()

Full name: `midgard.parsers._parser_rinex.parser_cache`

Signature: `(func: Callable[[ForwardRef('RinexParser'), Dict[str, str], List[Dict[str, str]]], Dict[str, Any]]) -> Callable[[ForwardRef('RinexParser'), Dict[str, str]], Dict[str, Any]]`

Decorator for adding a cache to parser functions

## midgard.parsers._parser_sinex
Basic functionality for parsing Sinex datafiles

**Description:**

This module contains functions and classes for parsing Sinex datafiles.


**References:**

* SINEX Format: https://www.iers.org/IERS/EN/Organization/AnalysisCoordinator/SinexFormat/sinex.html



### **SinexBlock**

Full name: `midgard.parsers._parser_sinex.SinexBlock`

Signature: `(marker: str, fields: Tuple[midgard.parsers._parser_sinex.SinexField, ...], parser: Callable[[<built-in function array>, Tuple[str, ...]], Dict[str, Any]])`

A convenience class for defining a Sinex block

**Args:**

- `marker`:  Sinex marker denoting the block.
- `fields`:  Fields in Sinex block.
- `parser`:  Function used to parse the data.


### **SinexField**

Full name: `midgard.parsers._parser_sinex.SinexField`

Signature: `(name: str, start_col: int, dtype: Optional[str], converter: Optional[str] = None)`

A convenience class for defining the fields in a Sinex block

**Args:**

- `name`:       Name of field.
- `start_col`:  Starting column of field (First column is 0)
- `dtype`:      String, using numpy notation, defining type of field, use None to ignore field.
- `converter`:  Optional, name of converter to apply to field data.


### **SinexParser**

Full name: `midgard.parsers._parser_sinex.SinexParser`

Signature: `(file_path: Union[str, pathlib.Path], encoding: Optional[str] = None, header: bool = True) -> None`

An abstract base class that has basic methods for parsing a Sinex file

This class provides functionality for parsing a sinex file with chained
groups of information. You should inherit from this one, and at least
specify which Sinex blocks you are interested in by implementing
`setup_parser`, as well as implement methods that parse each block if
needed.


### **parsing_factory**()

Full name: `midgard.parsers._parser_sinex.parsing_factory`

Signature: `() -> Callable[..., Dict[str, Any]]`

Create a default parsing function for a Sinex block

The default parsing function returns a dictionary containing all fields of
the block as separated arrays. This will be stored in self.data['{marker}']
with the {marker} of the current block.

**Returns:**

Simple parsing function for one Sinex block.


### **parsing_matrix_factory**()

Full name: `midgard.parsers._parser_sinex.parsing_matrix_factory`

Signature: `(marker: str, size_marker: str) -> Callable[..., Dict[str, Any]]`

Create a parsing function for parsing a matrix within a Sinex block

The default parsing function converts data to a symmetric matrix and stores
it inside `self.data[marker]`.

The size of the matrix is set to equal the number of parameters in the
`size_marker`-block. If that block is not parsed/found. The size is set to
the last given row index. If some zero elements in the matrix are omitted
this might be wrong.

**Args:**

- `marker`:       Marker of Sinex block.
- `size_marker`:  Marker of a different Sinex block indicating the size of the matrix.

**Returns:**

Simple parsing function for one Sinex block.


## midgard.parsers.antex
A parser for reading ANTEX format 1.4 data

**Example:**

    from midgard import parsers

    # Parse data
    p = parsers.parse_file(parser_name='antex', file_path='igs14.atx')

    # Get dictionary with parsed data
    data = p.as_dict()

**Description:**

Reads data from files in the GNSS Antenna Exchange (ANTEX) file format version 1.4 (see :cite:`antex`).



### **AntexParser**

Full name: `midgard.parsers.antex.AntexParser`

Signature: `(file_path: Union[str, pathlib.Path], encoding: Optional[str] = None) -> None`

A parser for reading ANTEX file

The parser reads GNSS ANTEX format 1.4 (see :cite:`antex`).

The 'data' attribute is a dictionary with GNSS satellite PRN or receiver antenna as key. The GNSS satellite
antenna corrections are time dependent and saved with "valid from" datetime object entry. The dictionary looks
like:

    dout = { <prn> : { <valid from>: { cospar_id:   <value>,
                                       sat_code:    <value>,
                                       sat_type:    <value>,
                                       valid_until: <value>,
                                       azimuth:     <list with azimuth values>,
                                       elevation:   <list with elevation values>,
                                       <frequency>: { azi: [<list with azimuth-elevation dependent corrections>],
                                                      neu: [north, east, up],
                                                      noazi: [<list with elevation dependent corrections>] }}},

             <receiver antenna> : { azimuth:     <list with azimuth values>,
                                    elevation:   <list with elevation values>,
                                    <frequency>: { azi: [<array with azimuth-elevation dependent corrections>],
                                                   neu: [north, east, up],
                                                   noazi: [<list with elevation dependent corrections>] }}}

with following entries:

| Value              | Type              | Description                                                            |
|--------------------|-------------------|------------------------------------------------------------------------|
| azi                | numpy.ndarray     | Array with azimuth-elevation dependent antenna correction in [mm] with |
|                    |                   | the shape: number of azimuth values x number of elevation values.      |
| azimuth            | numpy.ndarray     | List with azimuth values in [rad] corresponding to antenna corrections |
|                    |                   | given in `azi`.                                                        |
| cospar_id          | str               | COSPAR ID <yyyy-xxxa>: yyyy -> year when the satellite was put in      |
|                    |                   | orbit, xxx -> sequential satellite number for that year, a -> alpha    |
|                    |                   | numeric sequence number within a launch                                |
| elevation          | numpy.ndarray     | List with elevation values in [rad] corresponding to antenna           |
|                    |                   | corrections given in `azi` or `noazi`.                                 |
| <frequency>        | str               | Frequency identifier (e.g. G01 - GPS L1)                               |
| neu                | list              | North, East and Up eccentricities in [m]. The eccentricities of the    |
|                    |                   | mean antenna phase center is given relative to the antenna reference   |
|                    |                   | point (ARP) for receiver antennas or to the center of mass of the      |
|                    |                   | satellite in X-, Y- and Z-direction.                                   |
| noazi              | numpy.ndarray     | List with elevation dependent (non-azimuth-dependent) antenna          |
|                    |                   | correction in [mm].                                                    |
| <prn>              | str               | Satellite code e.g. GPS PRN, GLONASS slot or Galileo SVID number       |
| <receiver antenna> | str               | Receiver antenna name together with radome code                        |
| sat_code           | str               | Satellite code e.g. GPS SVN, GLONASS number or Galileo GSAT number     |
| sat_type           | str               | Satellite type (e.g. BLOCK IIA)                                        |
| valid_from         | datetime.datetime | Start of validity period of satellite in GPS time                      |
| valid_until        | datetime.datetime | End of validity period of satellite in GPS time                        |

The 'meta' attribute is a dictionary with following entries:

| Value          | Type | Description                                      |
|----------------|------|--------------------------------------------------|
| comment        | list | Header commments given in list line by line      |
| pcv_type       | str  | Phase center variation type                      |
| ref_antenna    | str  | Reference antenna type for relative antenna      |
| ref_serial_num | str  | Serial number of the reference antenna           |
| sat_sys        | str  | Satellite system                                 |
| version        | str  | Format version                                   |

**Attributes:**

- `data`:            (dict), Contains the (observation) data read from file.
- `data_available`:  (bool), Indicator of whether data are available.
- `file_path`:       (pathlib.Path), File path.
- `parser_name`:     (str), Parser name.
- `meta`:            (dict), Contains metainformation read from file.


## midgard.parsers.anubis
A parser for reading Anubis xtr-files


### **AnubisXtrParser**

Full name: `midgard.parsers.anubis.AnubisXtrParser`

Signature: `(file_path: Union[str, pathlib.Path], encoding: Optional[str] = None) -> None`

A parser for reading Anubis XTR files



## midgard.parsers.api_water_level_norway
A parser for reading water level data from open Norwegian water level API


**Example:**

    from datetime import datetime
    from midgard import parsers

    # XML file with water level data exists
    p = parsers.parse_file(parser_name='api_water_level_norway', file_path='api_water_level_norway')
    data = p.as_dict()

    # Water level data has to be downloaded from API
    p = parsers.parse_file(
                    parser_name='api_water_level_norway', 
                    file_path='api_water_level_norway',
                    latitude=58.974339,
                    longitude=5.730121,
                    from_date=datetime(2021,11,21),
                    to_date=datetime(2021,11,22),
    )
    data = p.as_dict()
    

**Description:**

See https://api.sehavniva.no/tideapi_no.html for an example


### **ApiWaterLevelNorwayParser**

Full name: `midgard.parsers.api_water_level_norway.ApiWaterLevelNorwayParser`

Signature: `(file_path: Union[str, pathlib.Path], encoding: Optional[str] = None, url: Optional[str] = None, latitude: Optional[float] = None, longitude: Optional[float] = None, from_date: Optional[datetime.datetime] = None, to_date: Optional[datetime.datetime] = None, reference_level: Optional[str] = 'chart_datum') -> None`

A parser for reading water level data from open Norwegian water level API

See https://api.sehavniva.no/tideapi_no.html for an example

Following **data** are available after water level data:

| Parameter           | Description                                                                           |
|---------------------|---------------------------------------------------------------------------------------|
| flag                | Data flag (obs: observation, pre: prediction, weather: weather effect, forecast:      |
|                     | forecast)                                                                             |
| time                | Observation                                                                           |
| water_level         | Water level in [cm]                                                                   |

and **meta**-data:

| Key                 | Description                                                                           |
|---------------------|---------------------------------------------------------------------------------------|
| __data_path__       | File path                                                                             |
| __parser_name__     | Parser name                                                                           |
| __url__             | URL of water level API                                                                |


## midgard.parsers.bcecmp_sisre
A parser for reading DLR BCEcmp Software SISRE output files

**Example:**

    from midgard import parsers
    p = parsers.parse_file(parser_name='bcecmp_sisre', file_path='BCEcmp_GAL_FNAV_E1E5A_com_2018_032.OUT')
    data = p.as_dict()

**Description:**

Reads data from files in the BCEcmp Software output file format. The BCEcmp Software is developed and used by DLR.



### **BcecmpParser**

Full name: `midgard.parsers.bcecmp_sisre.BcecmpParser`

Signature: `(file_path: Union[str, pathlib.Path], encoding: Optional[str] = None) -> None`

A parser for reading DLR BCEcmp Software output files.

The following **data** are available after reading BCEcmp Software output file:

| Key                   | Description                                                                          |
|-----------------------|--------------------------------------------------------------------------------------|
| age_min               | age of ephemeris in [min]                                                            |
| clk_diff_with_dt_mean | Satellite clock correction difference corrected for average satellite clock offset   |
|                       | difference for given GNSS and epoch in [m]                                           |
| dalong_track          | Along-track orbit difference in [m]                                                  |
| dcross_track          | Cross-track orbit difference in [m]                                                  |
| dradial               | Radial orbit difference in [m]                                                       |
| dradial_wul           | Worst-user-location (wul) SISRE?                                                     |
| satellite             | Satellite PRN number together with GNSS identifier (e.g. G07)                        |
| sisre                 | Signal-in-space range error [m]                                                      |
| time                  | Observation time                                                                     |
| used_iodc             | GPS: IODC (Clock issue of data indicates changes (set equal to IODE))                |
|                       | QZSS: IODC                                                                           |
| used_iode             | Ephemeris issue of data indicates changes to the broadcast ephemeris:                |
|                       |   - GPS: Ephemeris issue of data (IODE), which is set equal to IODC                  |
|                       |   - Galileo: Issue of Data of the NAV batch (IODnav)                                 |
|                       |   - QZSS: Ephemeris issue of data (IODE)                                             |
|                       |   - BeiDou: Age of Data Ephemeris (AODE)                                             |
|                       |   - IRNSS: Issue of Data, Ephemeris and Clock (IODEC)                                |

and **meta**-data:

| Key                   | Description                                                                          |
|-----------------------|--------------------------------------------------------------------------------------|
| \__data_path__        | File path                                                                            |
| \__parser_name__      | Parser name                                                                          |


## midgard.parsers.bernese_clu
A parser for reading Bernese CLU file

**Example:**

    from midgard import parsers
    p = parsers.parse_file(parser_name='bernese_clu', file_path='NOR_NKG.CLU')
    data = p.as_dict()

**Description:**

Reads data from files in Bernese CLU format.



### **BerneseCluParser**

Full name: `midgard.parsers.bernese_clu.BerneseCluParser`

Signature: `(file_path: Union[str, pathlib.Path], encoding: Optional[str] = None) -> None`

A parser for reading Bernese CLU file

Following **data** are available after reading Bernese CLU file:

| Parameter           | Description                                                                           |
|---------------------|---------------------------------------------------------------------------------------|
| station             | 4-digit station identifier                                                            |
| domes               | Domes number                                                                          |
| cluster             | Cluster number                                                                        |

and **meta**-data:

| Key                  | Description                                                                          |
|----------------------|--------------------------------------------------------------------------------------|
| \__data_path__       | File path                                                                            |
| \__parser_name__     | Parser name                                                                          |



## midgard.parsers.bernese_compar_out
A parser for reading coordinate comparison in Bernese OUT format


**Example:**

    from midgard import parsers
    p = parsers.parse_file(parser_name='bernese_compar_out', file_path='COMP211670.OUT')
    data = p.as_dict()

**Description:**

Reads coordinate comparison data from files in OUT format



### **BerneseComparOutParser**

Full name: `midgard.parsers.bernese_compar_out.BerneseComparOutParser`

Signature: `(*args: Tuple[Any], **kwargs: Dict[Any, Any])`

A parser for reading coordinate comparison in Bernese OUT format


The parsed data are saved in variable **data** as a dictionay with 4-digit station name as key. The station
related data are saved in a dictionary with following keys:

| Key                   | Type        |Description                                                           |
|-----------------------|-------------|----------------------------------------------------------------------|
| coord_comp_east       | List[float] | List with daily station coordinate comparison results for East       |
|                       |             | component in [m]                                                     |
| coord_comp_north      | List[float] | List with daily station coordinate comparison results for North      |
|                       |             | component in [m]                                                     |
| coord_comp_up         | List[float] | List with daily station coordinate comparison results for Up         |
|                       |             | component in [m]                                                     |
| coord_comp_rms_east   | float       | List with daily station coordinate comparison results for East       |
|                       |             | component in [m]                                                     |
| coord_comp_rms_north  | float       | List with daily station coordinate comparison results for North      |
|                       |             | component in [m]                                                     |
| coord_comp_rms_up     | float       | List with daily station coordinate comparison results for Up         |
|                       |             | component in [m]                                                     |
| pos_mean_x            | float       | X-coordinate of mean station coordinate position in [m]              |
| pos_mean_x_rms1       | float       | RMS1 of X-coordinate of mean station coordinate position in [m]      |
| pos_mean_x_rms2       | float       | RMS2 of X-coordinate of mean station coordinate position in [m]      |
| pos_mean_y            | float       | Y-coordinate of mean station coordinate position in [m]              |
| pos_mean_y_rms1       | float       | RMS1 of Y-coordinate of mean station coordinate position in [m]      |
| pos_mean_y_rms2       | float       | RMS2 of Y-coordinate of mean station coordinate position in [m]      |
| pos_mean_z            | float       | Z-coordinate of mean station coordinate position in [m]              |
| pos_mean_z_rms1       | float       | RMS1 of Z-coordinate of mean station coordinate position in [m]      |
| pos_mean_z_rms2       | float       | RMS2 of Z-coordinate of mean station coordinate position in [m]      |

and **meta**-data:

| Key                  | Description                                                                          |
|----------------------|--------------------------------------------------------------------------------------|
| num_coord_files      | Number of coordinate files used for analysis                                         |
| time                 | Date of analysis session                                                             |
| \__data_path__       | File path                                                                            |
| \__parser_name__     | Parser name                                                                          |


## midgard.parsers.bernese_crd
A parser for reading Bernese CRD file

**Example:**

    from midgard import parsers
    p = parsers.parse_file(parser_name='bernese_crd', file_path='W20216.CRD')
    data = p.as_dict()

**Description:**

Reads data from files in Bernese CRD format.



### **BerneseCrdParser**

Full name: `midgard.parsers.bernese_crd.BerneseCrdParser`

Signature: `(file_path: Union[str, pathlib.Path], encoding: Optional[str] = None) -> None`

A parser for reading Bernese CRD file

Following **data** are available after reading Bernese CRD file:

| Parameter           | Description                                                                           |
|---------------------|---------------------------------------------------------------------------------------|
| num                 | Number of station coordinate solution                                                 |
| station             | 4-digit station identifier                                                            |
| domes               | Domes number                                                                          |
| gpssec              | Seconds of GPS week                                                                   |
| pos_x               | X-coordinate of station position                                                      |
| pos_y               | Y-coordinate of station position                                                      |
| pos_z               | Z-coordinate of station position                                                      |
| flag                | Flag                                                                                  |

and **meta**-data:

| Key                  | Description                                                                          |
|----------------------|--------------------------------------------------------------------------------------|
| \__data_path__       | File path                                                                            |
| \__params__          | np.genfromtxt parameters                                                             |
| \__parser_name__     | Parser name                                                                          |



## midgard.parsers.bernese_prc
A parser for reading protocol file in Bernese PRC format


**Example:**

    from midgard import parsers
    p = parsers.parse_file(parser_name='bernese_prc', file_path='RES211670.PRC')
    data = p.as_dict()

**Description:**

Reads data from files in PRC format



### **BernesePrcParser**

Full name: `midgard.parsers.bernese_prc.BernesePrcParser`

Signature: `(*args: Tuple[Any], **kwargs: Dict[Any, Any])`

A parser for reading protocol file in Bernese PRC format


The parsed data are saved in variable **data** as a dictionay with 4-digit station name as key. The station
related data are saved in a dictionary with following keys:

| Key                   | Type        |Description                                                           |
|-----------------------|-------------|----------------------------------------------------------------------|
| coord_comp_east       | List[float] | List with daily station coordinate comparison results for East       |
|                       |             | component in [m]                                                     |
| coord_comp_north      | List[float] | List with daily station coordinate comparison results for North      |
|                       |             | component in [m]                                                     |
| coord_comp_up         | List[float] | List with daily station coordinate comparison results for Up         |
|                       |             | component in [m]                                                     |
| coord_comp_rms_east   | float       | List with daily station coordinate comparison results for East       |
|                       |             | component in [m]                                                     |
| coord_comp_rms_north  | float       | List with daily station coordinate comparison results for North      |
|                       |             | component in [m]                                                     |
| coord_comp_rms_up     | float       | List with daily station coordinate comparison results for Up         |
|                       |             | component in [m]                                                     |
| num_of_days           | float       | Number of days used for analysis                                     |
| pos_mean_x            | float       | X-coordinate of mean station coordinate position in [m]              |
| pos_mean_x_rms1       | float       | RMS1 of X-coordinate of mean station coordinate position in [m]      |
| pos_mean_x_rms2       | float       | RMS2 of X-coordinate of mean station coordinate position in [m]      |
| pos_mean_y            | float       | Y-coordinate of mean station coordinate position in [m]              |
| pos_mean_y_rms1       | float       | RMS1 of Y-coordinate of mean station coordinate position in [m]      |
| pos_mean_y_rms2       | float       | RMS2 of Y-coordinate of mean station coordinate position in [m]      |
| pos_mean_z            | float       | Z-coordinate of mean station coordinate position in [m]              |
| pos_mean_z_rms1       | float       | RMS1 of Z-coordinate of mean station coordinate position in [m]      |
| pos_mean_z_rms2       | float       | RMS2 of Z-coordinate of mean station coordinate position in [m]      |
| repeatability_east    | float       | Station coordinate repeatability for East component in [m]           |
| repeatability_north   | float       | Station coordinate repeatability for North component in [m]          |
| repeatability_up      | float       | Station coordinate repeatability for Up component in [m]             |
| residual_east         | float       | Station residuals for East component in [m]                          |
| residual_north        | float       | Station residuals for North component in [m]                         |
| residual_up           | float       | Station residuals for Up component in [m]                            |

and **meta**-data:

| Key                  | Description                                                                          |
|----------------------|--------------------------------------------------------------------------------------|
| num_coord_files      | Number of coordinate files used for analysis                                         |
| time                 | Date of analysis session                                                             |
| \__data_path__       | File path                                                                            |
| \__parser_name__     | Parser name                                                                          |


## midgard.parsers.bernese_slr_plt
A parser for reading Bernese SLR PLT file

**Example:**

    from midgard import parsers
    p = parsers.parse_file(parser_name='bernese_slr_plt', file_path='SLR_20232580.PLT')
    data = p.as_dict()

**Description:**

Reads data from files in Bernese PLT format.



### **BerneseSlrPltParser**

Full name: `midgard.parsers.bernese_slr_plt.BerneseSlrPltParser`

Signature: `(file_path: Union[str, pathlib.Path], encoding: Optional[str] = None) -> None`

A parser for reading Bernese SLR PLT file

Following **data** are available after reading Bernese PLT file:

| Parameter          | Description                                                                    |
|--------------------|--------------------------------------------------------------------------------|
| station            | 4-digit station identifier                                                     |
| domes              | domes number, e.g.  50107M001                                                  |
| sat_prn            | satellite, e.g. E18
| epoch              | mjd of observation                                                             |
| residual           | observation residual (mm)                                                      |
| azi                | azimuth (deg)                                                                  |
| ele                | elevation (deg)


and **meta**-data:

| Key                  | Description                                                                          |
|----------------------|--------------------------------------------------------------------------------------|
| \__data_path__       | File path                                                                            |
| \__params__          | np.genfromtxt parameters                                                             |
| \__parser_name__     | Parser name                                                                          |



## midgard.parsers.bernese_sta
A parser for reading station information in Bernese STA format


**Example:**

    from midgard import parsers
    p = parsers.parse_file(parser_name='bernese_sta', file_path='NKG.STA')
    data = p.as_dict()

**Description:**

Reads station information from files in STA format, whereby at the moment only the 'STATION INFORMATION' part is
parsed.



### **BerneseStaParser**

Full name: `midgard.parsers.bernese_sta.BerneseStaParser`

Signature: `(*args: Tuple[Any], **kwargs: Dict[Any, Any])`

A parser for reading station information in Bernese STA format


The parsed data are saved in variable **data** as a dictionay with 4-digit station name as key and a list with 
station information dictionaries with following entries:

| Key                          | Type     |Description                                                         |
|------------------------------|----------|--------------------------------------------------------------------|
| antenna_serial_number        | str      | Antenna serial number                                              |
| antenna_serial_number_short  | str      | 6 last digits of antennna serial number                            |
| antenna_type                 | str      | Antenna type                                                       |
| date_from                    | datetime | Start date where station information is valid                      |
| date_to                      | datetime | End date of station information                                    | 
| domes                        | str      | Domes number                                                       |
| description                  | str      | Description normally with station name and country code            |
| eccentricity_east            | float    | East component of eccentricity in [m]                              |
| eccentricity_north           | float    | North component of eccentricity in [m]                             |
| eccentricity_up              | float    | Up component of eccentricity in [m]                                |
| flag                         | str      | Flag number                                                        |
| radome                       | str      | Antenna radome type                                                |
| receiver_serial_number       | str      | Receiver serial number                                             |
| receiver_serial_number_short | str      | 6 last digits of receiver serial number                            |
| receiver_type                | str      | Receiver type                                                      |
| remark                       | str      | Remark                                                             |

and **meta**-data:

| Key                  | Description                                                                        |
|----------------------|------------------------------------------------------------------------------------|
| \__data_path__       | File path                                                                          |
| \__parser_name__     | Parser name                                                                        |


## midgard.parsers.bernese_trp
A parser for reading troposphere files in Bernese TRP format


**Example:**

    from analyx import parsers
    p = parsers.parse_file(parser_name='bernese_trp', file_path='F1_210300.TRP')
    data = p.as_dict()

**Description:**

Reads data from files troposphere files in TRP format



### **BerneseTrpPaser**

Full name: `midgard.parsers.bernese_trp.BerneseTrpPaser`

Signature: `(file_path: Union[str, pathlib.Path], encoding: Optional[str] = None) -> None`

A parser for reading troposphere files in Bernese TRP format


Following **data** can be available after reading troposphere files in Bernese TRP file:

| Key                  | Description                                                                          |
| :------------------- | :----------------------------------------------------------------------------------- |
| TODO                 |                                                                                      |

and **meta**-data:

| Key                  | Description                                                                          |
| :------------------- | :----------------------------------------------------------------------------------- |
| TODO                 |                                                                                      |
| \__data_path__       | File path                                                                            |
| \__params__          | np.genfromtxt parameters                                                             |
| \__parser_name__     | Parser name                                                                          |


## midgard.parsers.cost
A parser for reading COST format for ground-based GNSS delay and water vapour data

**Example:**

    from midgard import parsers
    
    # Parse data
    parser = parsers.parse_file(parser_name="cost", file_path=file_path)
    
    # Get Dataset with parsed data
    dset = parser.as_dataset()

**Description:**

Reads data from files in the COST file format 2.2a (see :cite:`cost`).



### **CostParser**

Full name: `midgard.parsers.cost.CostParser`

Signature: `(file_path: Union[str, pathlib.Path], encoding: Optional[str] = None) -> None`

A parser for reading COST datan file

The parser reads ground-based GNSS delay and water vapour data in COST format version 2.2a.

**Attributes:**

data (Dict):                  The (observation) data read from file.
data_available (Boolean):     Indicator of whether data are available.
file_encoding (String):       Encoding of the datafile.
file_path (Path):             Path to the datafile that will be read.
meta (Dict):                  Metainformation read from file.
parser_name (String):         Name of the parser (as needed to call parsers.parse_...).


### UNIT_DEF (dict)
`UNIT_DEF = {'height_geoid': UnitField(from_='meter', to_='meter'), 'humidity': UnitField(from_='', to_=''), 'iwv': UnitField(from_='kilogram/meter**2', to_='kilogram/meter**2'), 'pressure': UnitField(from_='hectopascal', to_='pascal'), 'temperature': UnitField(from_='kelvin', to_='kelvin'), 'trop_gradient_east': UnitField(from_='millimeter', to_='meter'), 'trop_gradient_east_sigma': UnitField(from_='millimeter', to_='meter'), 'trop_gradient_north': UnitField(from_='millimeter', to_='meter'), 'trop_gradient_north_sigma': UnitField(from_='millimeter', to_='meter'), 'trop_zenith_total': UnitField(from_='millimeter', to_='meter'), 'trop_zenith_total_sigma': UnitField(from_='millimeter', to_='meter'), 'trop_zenith_wet': UnitField(from_='millimeter', to_='meter')}`


### **UnitField**

Full name: `midgard.parsers.cost.UnitField`

Signature: `(from_=None, to_=None)`

A convenience class for defining a COST units of fields

**Args:**

from (str):              Original field unit
to (str):                Destination field unit


## midgard.parsers.csv_
A parser for reading CSV output files

**Example:**

    from midgard import parsers
    p = parsers.parse_file(parser_name='csv_', file_path='ADOP20473_0000.csv')
    data = p.as_dict()

**Description:**

Reads data from files in CSV output format. The header information of the CSV file is not read (TODO).



### **CsvParser**

Full name: `midgard.parsers.csv_.CsvParser`

Signature: `(file_path: Union[str, pathlib.Path], encoding: Optional[str] = None) -> None`

A parser for reading CSV output files

The CSV data header line is used to define the keys of the **data** dictionary. The values of the **data** 
dictionary are represented by the CSV colum values.

Following **meta**-data are available after reading of CSV file:

| Key                  | Description                                                                          |
|----------------------|--------------------------------------------------------------------------------------|
| \__data_path__       | File path                                                                            |
| \__parser_name__     | Parser name                                                                          |


## midgard.parsers.galileo_constellation_html
A parser for reading Galileo constellation info from a web page

See https://www.gsc-europa.eu/system-status/Constellation-Information for an example


### **GalileoConstellationHTMLParser**

Full name: `midgard.parsers.galileo_constellation_html.GalileoConstellationHTMLParser`

Signature: `(file_path: Union[str, pathlib.Path], encoding: Optional[str] = None, url: Optional[str] = None) -> None`

A parser for reading Galileo constellation info from a web page

See https://www.gsc-europa.eu/system-status/Constellation-Information for an example


## midgard.parsers.gamit_org
A parser for reading Gamit ORG files

**Example:**

    from midgard import parsers

    # Parse data
    parser = parsers.parse_file(parser_name="gamit_org", file_path=file_path)

    # Get Dataset with parsed data
    dset = parser.as_dataset()

**Description:**

Reads the output file of Gamit.

Example header from wich the time information is read from the .org file

---------------------------------------------------------
 GLOBK Ver 5.34, Global solution
---------------------------------------------------------

 Solution commenced with: 2022/ 6/22  0: 0    (2022.4712)
 Solution ended with    : 2022/ 6/22 23:59    (2022.4740)
 Solution refers to     : 2022/ 6/22 11:59    (2022.4726) [Seconds tag  45.000]
 Satellite IC epoch     : 2022/ 6/22 12: 0  0.00


Example lines to be read from the .org file

    REYK_JPS X coordinate  (m)          2587383.93370     -0.01703      0.00446

    REYK_JPS Y coordinate  (m)         -1043033.57942     -0.04451      0.00404

    REYK_JPS Z coordinate  (m)          5716564.17515      0.00474      0.00947


### **GamitOrgParser**

Full name: `midgard.parsers.gamit_org.GamitOrgParser`

Signature: `(file_path: Union[str, pathlib.Path], encoding: Optional[str] = None) -> None`

A parser for reading gamit org file

**Attributes:**

data (Dict):                  The (observation) data read from file.
file_path (Path):             Path to the datafile that will be read.
meta (Dict):                  Metainformation read from file.
parser_name (String):         Name of the parser (as needed to call parsers.parse_...).
system (String):              GNSS identifier.

Methods:
    as_dataset()                  Return the parsed data as a Midgard Dataset
    parse()                       Parse data
    setup_parser()                Set up information needed for the parser

    _parse_time()                 Parse a line of time information
    _parse_station()              Parse a line of station information


## midgard.parsers.gipsy_stacov
A parser for reading NASA JPL Gipsy `stacov` format file

`stacov` format file includes Gipsy estimates and covariance information. 

**Example:**

    from midgard import parsers
    p = parsers.parse_file(parser_name='gipsy_stacov', file_path='stacov_final')
    data = p.as_dict()

**Description:**

Reads data from files in Gipsy `stacov` format.



### **GipsyStacovParser**

Full name: `midgard.parsers.gipsy_stacov.GipsyStacovParser`

Signature: `(file_path: Union[str, pathlib.Path], encoding: Optional[str] = None) -> None`

A parser for reading Gipsy `stacov` format file

Following **data** are available after reading Gipsy `stacov` output file:

| Key                  | Description                                                                          |
|----------------------|--------------------------------------------------------------------------------------|
| correlation          | Correlation values                                                                   |
| correlation_index1   | Correlation index (1st column)                                                       |
| correlation_index2   | Correlation index (2nd column)                                                       |
| estimate             | Parameter estimate at the given time                                                 |
| estimate_index       | Estimate index                                                                       |
| parameter            | Parameter name. An arbitrary sequence of letters [A-Z,a-z], digits[0-9], and "."     |
|                      | without spaces.                                                                      |
| row                  | Row number of correlations                                                           |
| station              | Station name.                                                                        |    
| sigma                | Standard deviation of the parameter.                                                 |
| time_past_j2000      | Time given in GPS seconds past J2000, whereby GipsyX uses following definition:      |
|                      | J2000 is continuous seconds past Jan. 1, 2000 11:59:47 UTC.                          |



and **meta**-data:

| Key                  | Description                                                                          |
|----------------------|--------------------------------------------------------------------------------------|
| \__data_path__       | File path                                                                            |
| \__parser_name__     | Parser name                                                                          |


## midgard.parsers.gipsy_sum
A parser for reading Gipsy summary output file (*.sum)

**Example:**

    from midgard import parsers
    p = parsers.parse_file(parser_name='gipsy_sum', file_path='gipsy_sum')
    data = p.as_dict()

**Description:**

Reads data from files in Gipsy summary output format.



### **GipsySummary**

Full name: `midgard.parsers.gipsy_sum.GipsySummary`

Signature: `(file_path: Union[str, pathlib.Path], encoding: Optional[str] = None) -> None`

A parser for reading Gipsy summary output file (*.sum)

Gipsy summary file **data** are grouped as follows:

| Key                   | Description                                                                          |
| :-------------------- | :----------------------------------------------------------------------------------- |
| date                  | Processing date                                                                      |
| residual              | Dictionary with residual summary information                                         |
| station               | Station name                                                                         |

**residual** entries are:

| Key                   | Description                                                                          |
| :-------------------- | :----------------------------------------------------------------------------------- |
| code_obs_num          | Number of used pseudo-range observations                                             |
| code_outlier_num      | Number of rejected pseudo-range observations                                         |
| code_residual_rms     | RMS of residuals from used pseudo-range observations in [m]                          |
| phase_obs_num         | Number of used phase observations                                                    |
| phase_outlier_num     | Number of rejected phase observations                                                |
| phase_residual_rms    | RMS of residuals from used phase observations in [m]                                 |

and **meta**-data:

| Key                  | Description                                                                          |
| :------------------- | :----------------------------------------------------------------------------------- |
| \__data_path__       | File path                                                                            |
| \__parser_name__     | Parser name                                                                          |


## midgard.parsers.gipsy_tdp
A parser for reading NASA JPL Gipsy time dependent parameter (TDP) file

**Example:**

    from midgard import parsers
    p = parsers.parse_file(parser_name='gipsy_tdp', file_path='final.tdp')
    data = p.as_dict()

**Description:**

Reads data from files in Gipsy time dependent parameter (TDP) format.



### **DatasetField**

Full name: `midgard.parsers.gipsy_tdp.DatasetField`

Signature: `(name=None, dtype=None)`

A convenience class for defining a dataset field properties

**Args:**

name  (str):             Dataset field name
dtype (str):             Dataset data type


### **GipsyTdpParser**

Full name: `midgard.parsers.gipsy_tdp.GipsyTdpParser`

Signature: `(file_path: Union[str, pathlib.Path], encoding: Optional[str] = None) -> None`

A parser for reading Gipsy time dependent parameter (TDP) file

Following **data** are available after reading Gipsy TDP output file:

| Key                  | Description                                                                          |
|----------------------|--------------------------------------------------------------------------------------|
| apriori              | Nominal value. This field contains the last value used by the model.                 |
| name                 | Parameter name.                                                                      |
| sigma                | The sigma associated with the value of the parameter. A negative value indicates it  |
|                      | should be used for interpolation by the file reader read_time_variation in           |
|                      | $GOA/libsrc/time_variation. If no sigmas are computed by the smapper, a 1.0 will be  |
|                      | placed here.                                                                         |
| time_past_j2000      | Time given in GPS seconds past J2000.                                                |
| value                | Accumulated value of the parameter at time and includes any nominal, or iterative    |
|                      | correction. This is the only entry used by the model.                                |

and **meta**-data:

| Key                  | Description                                                                          |
|----------------------|--------------------------------------------------------------------------------------|
| \__data_path__       | File path                                                                            |
| \__parser_name__     | Parser name                                                                          |


## midgard.parsers.gipsyx_gdcov
A parser for reading NASA JPL GipsyX `gdcov` format file

`gdcov` format file includes GipsyX estimates and covariance information. 

NOTE: At the moment this parser can only read station estimate and covariance information, that means STA.X, STA.Y 
      and STA.Z parameters.

**Example:**

    from midgard import parsers
    p = parsers.parse_file(parser_name='gipsyx_gdcov', file_path='smoothFinal.gdcov')
    data = p.as_dict()

**Description:**

Reads data from files in GipsyX `gdcov` format.



### **GipsyxGdcovParser**

Full name: `midgard.parsers.gipsyx_gdcov.GipsyxGdcovParser`

Signature: `(file_path: Union[str, pathlib.Path], encoding: Optional[str] = None) -> None`

A parser for reading GipsyX `gdcov` format file

Following **data** are available after reading GipsyX `gdcov` output file:

| Key                  | Description                                                                          |
|----------------------|--------------------------------------------------------------------------------------|
| correlation          | Correlation values                                                                   |
| correlation_index1   | Correlation index (1st column)                                                       |
| correlation_index2   | Correlation index (2nd column)                                                       |
| estimate             | Parameter estimate at the given time                                                 |
| estimate_index       | Estimate index                                                                       |
| parameter            | Parameter name. An arbitrary sequence of letters [A-Z,a-z], digits[0-9], and "."     |
|                      | without spaces.                                                                      |
| row                  | Row number of correlations                                                           |
| station              | Station name.                                                                        |    
| sigma                | Standard deviation of the parameter.                                                 |
| time_past_j2000      | Time given in GPS seconds past J2000, whereby GipsyX uses following definition:      |
|                      | J2000 is continuous seconds past Jan. 1, 2000 11:59:47 UTC.                          |



and **meta**-data:

| Key                  | Description                                                                          |
|----------------------|--------------------------------------------------------------------------------------|
| \__data_path__       | File path                                                                            |
| \__parser_name__     | Parser name                                                                          |


## midgard.parsers.gipsyx_residual
A parser for reading NASA JPL GipsyX residual file

**Example:**

    from midgard import parsers
    p = parsers.parse_file(parser_name='gipsyx_residual', file_path='finalResiduals.out')
    data = p.as_dict()

**Description:**

Reads data from files in GipsyX residual format.



### **GipsyxResidualParser**

Full name: `midgard.parsers.gipsyx_residual.GipsyxResidualParser`

Signature: `(file_path: Union[str, pathlib.Path], encoding: Optional[str] = None) -> None`

A parser for reading GipsyX residual file

Following **data** are available after reading GipsyX residual output file:

| Key                  | Description                                                                          |
|----------------------|--------------------------------------------------------------------------------------|
| azimuth              | Azimuth from receiver                                                                |
| azimuth_sat          | Azimuth from satellite                                                               |
| data_type            | Data type (e.g. IonoFreeC_1P_2P, IonoFreeL_1P_2P)                                    |
| deleted              | Residuals are deleted, marked with True or False.                                    |
| elevation            | Elevation from receiver                                                              |
| elevation_sat        | Elevation from satellite                                                             |
| residual             | Post-fit residual                                                                    |
| satellite            | Satellite name                                                                       |
| station              | Station name                                                                         |
| time_past_j2000      | Time given in GPS seconds past J2000, whereby GipsyX uses following definition:      |
|                      | J2000 is continuous seconds past Jan. 1, 2000 11:59:47 UTC.                          |


and **meta**-data:

| Key                  | Description                                                                          |
|----------------------|--------------------------------------------------------------------------------------|
| \__data_path__       | File path                                                                            |
| \__parser_name__     | Parser name                                                                          |


## midgard.parsers.gipsyx_series
A parser for reading NASA JPL GipsyX timeseries file

**Example:**

    from analyx import parsers
    p = parsers.parse_file(parser_name='gipsyx_series', file_path='NYA1.series')
    data = p.as_dict()

**Description:**

Reads data from files in GipsyX timeseries format.



### **GipsyxSeriesParser**

Full name: `midgard.parsers.gipsyx_series.GipsyxSeriesParser`

Signature: `(file_path: Union[str, pathlib.Path], encoding: Optional[str] = None) -> None`

A parser for reading GipsyX timeseries file

Following **data** are available after reading GipsyX residual output file:


| Key                  | Description                                                                          |
|----------------------|--------------------------------------------------------------------------------------|
| corr_en              | Correlation East-North.                                                              |
| corr_ev              | Correlation East-Vertical.                                                           |
| corr_nv              | Correlation North-Vertical.                                                          |
| day                  | Day                                                                                  |
| decimalyear          | Date in unit year.                                                                   |
| east                 | East coordinate in [m].                                                              |
| east_sigma           | Standard devication of east coordinate in [m].                                       |
| hour                 | Hour                                                                                 |
| minute               | Minute                                                                               |
| month                | Month                                                                                |
| north                | North coordinate in [m].                                                             |
| north_sigma          | Standard devication of north coordinate in [m].                                      |
| second               | Second                                                                               |
| time_past_j2000      | Time given in GPS seconds past J2000, whereby GipsyX uses following definition:      |
|                      | J2000 is continuous seconds past Jan. 1, 2000 11:59:47 UTC.                          |
| vertical             | Vertical coordinate in [m].                                                          |
| vertical_sigma       | Standard devication of vertical coordinate in [m].                                   |
| year                 | Year                                                                                 |

and **meta**-data:

| Key                  | Description                                                                          |
|----------------------|--------------------------------------------------------------------------------------|
| \__data_path__       | File path                                                                            |
| \__parser_name__     | Parser name                                                                          |


## midgard.parsers.gipsyx_summary
A parser for reading GipsyX summary output file

**Example:**

    from midgard import parsers
    p = parsers.parse_file(parser_name='gipsyx_summary', file_path='gipsyx_summary')
    data = p.as_dict()

**Description:**

Reads data from files in GipsyX summary output format.



### **GipsyxSummary**

Full name: `midgard.parsers.gipsyx_summary.GipsyxSummary`

Signature: `(file_path: Union[str, pathlib.Path], encoding: Optional[str] = None) -> None`

A parser for reading GipsyX summary file

GipsyX summary file **data** are grouped as follows:

| Key                   | Description                                                                          |
|-----------------------|--------------------------------------------------------------------------------------|
| position              | Dictionary with position summary information                                         |
| residual              | Dictionary with residual summary information                                         |
| station               | Station name                                                                         |

**position** entries are:

| Key                   | Description                                                                          |
|-----------------------|--------------------------------------------------------------------------------------|
| pos_x                 | X-coordinate of station position solution                                            |
| pos_y                 | Y-coordinate of station position solution                                            |
| pos_z                 | Z-coordinate of station position solution                                            |
| pos_vs_ref_x          | X-coordinate of difference between solution and reference of station coordinate      |
| pos_vs_ref_y          | Y-coordinate of difference between solution and reference of station coordinate      |
| pos_vs_ref_z          | Z-coordinate of difference between solution and reference of station coordinate      |
| pos_vs_ref_e          | East-coordinate of difference between solution and reference of station coordinate   |
| pos_vs_ref_n          | North-coordinate of difference between solution and reference of station coordinate  |
| pos_vs_ref_v          | Vertical-coordinate of difference between solution and reference of station          |
|                       | coordinate                                                                           |


**residual** entries are:

| Key                   | Description                                                                          |
|-----------------------|--------------------------------------------------------------------------------------|
| code_obs_num          | Number of used pseudo-range observations                                             |
| code_residual_max     | Maximal residual of used pseudo-range observations                                   |
| code_residual_min     | Minimal residual of used pseudo-range observations                                   |
| code_residual_rms     | RMS of residuals from used pseudo-range observations                                 |
| code_outlier_max      | Maximal residual of rejected pseudo-range observations                               |
| code_outlier_min      | Minimal residual of rejected pseudo-range observations                               |
| code_outlier_num      | Number of rejected pseudo-range observations                                         |
| code_outlier_rms      | RMS of residuals from rejected pseudo-range observations                             |
| phase_obs_num         | Number of used phase observations                                                    |
| phase_residual_min    | Minimal residual of used phase observations                                          |
| phase_residual_max    | Maximal residual of used phase observations                                          |
| phase_residual_rms    | RMS of residuals from used phase observations                                        |
| phase_outlier_max     | Maximal residual of rejected phase observations                                      |
| phase_outlier_min     | Minimal residual of rejected phase observations                                      |
| phase_outlier_num     | Number of rejected phase observations                                                |
| phase_outlier_rms     | RMS of residuals from rejected phase observations                                    |


and **meta**-data:

| Key                  | Description                                                                          |
|----------------------|--------------------------------------------------------------------------------------|
| \__data_path__       | File path                                                                            |
| \__parser_name__     | Parser name                                                                          |


## midgard.parsers.gipsyx_tdp
A parser for reading NASA JPL GipsyX time dependent parameter (TDP) file

**Example:**

    from midgard import parsers
    p = parsers.parse_file(parser_name='gipsyx_tdp', file_path='final.tdp')
    data = p.as_dict()

**Description:**

Reads data from files in GipsyX time dependent parameter (TDP) format.



### **DatasetField**

Full name: `midgard.parsers.gipsyx_tdp.DatasetField`

Signature: `(name=None, category=None, dtype=None)`

A convenience class for defining a dataset field properties

**Args:**

name  (str):             Dataset field name
category (str):          Category of parameter (e.g. station or satellite parameter)
dtype (str):             Dataset data type


### **GipsyxTdpParser**

Full name: `midgard.parsers.gipsyx_tdp.GipsyxTdpParser`

Signature: `(file_path: Union[str, pathlib.Path], encoding: Optional[str] = None) -> None`

A parser for reading GipsyX time dependent parameter (TDP) file

Following **data** are available after reading GipsyX TDP output file:

| Key                  | Description                                                                          |
|----------------------|--------------------------------------------------------------------------------------|
| apriori              | Nominal value. This field contains the last value used by the model.                 |
| name                 | Parameter name. An arbitrary sequence of letters [A-Z,a-z], digits[0-9], and "."     |
|                      | without spaces.                                                                      |
| sigma                | Standard deviation of the parameter.                                                 |
| time_past_j2000      | Time given in GPS seconds past J2000, whereby GipsyX uses following definition:      |
|                      | J2000 is continuous seconds past Jan. 1, 2000 11:59:47 UTC.                          |
| value                | Parameter value at the given time                                                    |

and **meta**-data:

| Key                  | Description                                                                          |
|----------------------|--------------------------------------------------------------------------------------|
| \__data_path__       | File path                                                                            |
| \__parser_name__     | Parser name                                                                          |


## midgard.parsers.glab_output
A parser for reading gLAB output files

**Example:**

    from midgard import parsers
    p = parsers.parse_file(parser_name='glab_output', file_path='glab_output.txt')
    data = p.as_dict()

**Description:**




### **GlabOutputParser**

Full name: `midgard.parsers.glab_output.GlabOutputParser`

Signature: `(file_path: Union[str, pathlib.Path], encoding: Optional[str] = None) -> None`

A parser for reading gLAB output files

The keys of the **data** dictionary are defined depending, which kind of gLAB output file is read. The values of 
the **data** dictionary are represented by the gLAB colum values.

Following **meta**-data are available after reading of gLAB files:

| Key                  | Description                                                                          |
|----------------------|--------------------------------------------------------------------------------------|
| \__data_path__       | File path                                                                            |
| \__parser_name__     | Parser name                                                                          |


## midgard.parsers.gnss_android_raw_data
A parser for reading GNSS raw data from `GnssLogger` Android App

**Example:**
    
    from midgard import parsers
    
    # Parse data
    parser = parsers.parse_file(parser_name="gnss_android_raw_data", file_path=file_path)
    
    # Get Dataset with parsed data
    dset = parser.as_dataset()

**Description:**

Reads raw data file from `GnssLogger` Android App.



### **GnssAndroidRawDataParser**

Full name: `midgard.parsers.gnss_android_raw_data.GnssAndroidRawDataParser`

Signature: `(file_path: Union[str, pathlib.Path], encoding: Optional[str] = None) -> None`



## midgard.parsers.gnss_galat_results
A parser for GALAT single point positioning result files

**Example:**

    from midgard import parsers
    p = parsers.parse_file(parser_name='gnss_galat_results', file_path='galat_results.txt')
    data = p.as_dict()

**Description:**

Reads data from files in GALAT result format.



### **GalatResults**

Full name: `midgard.parsers.gnss_galat_results.GalatResults`

Signature: `(file_path: Union[str, pathlib.Path], encoding: Optional[str] = None) -> None`

A parser for reading GALAT single point positioning result files

Following **data** are available after reading GALAT SPP result file:

| Key                      | Description                                                                      |
|--------------------------|----------------------------------------------------------------------------------|
| time                     | Time epoch                                                                       |
| latitude                 | Latitude in degree                                                               |
| longitude                | Longitude in degree                                                              |
| height                   | Height in [m]                                                                    |
| dlatitude                | Latitude related to reference coordinate in [m]                                  |
| dlongitude               | Longitude related to reference coordinate in [m]                                 |
| dheight                  | Height related to reference coordinate in [m]                                    |
| hpe                      | Horizontal positioning error (HPE) in [m]                                        |
| vpe                      | Vertical positioning error (VPE) in [m]                                          |
| site_vel_3d              | 3D site velocity in [m/s]                                                        |
| pdop                     | Precision dilution of precision                                                  |
| num_satellite_available  | Number of available satellites                                                   |
| num_satellite_used       | Number of used satellites                                                        |


and **meta**-data:

| Key                  | Description                                                                          |
|----------------------|--------------------------------------------------------------------------------------|
| \__data_path__       | File path                                                                            |
| \__params__          | np.genfromtxt parameters                                                             |
| \__parser_name__     | Parser name                                                                          |


## midgard.parsers.gnssrefl_allrh
A parser for reading GNSSREFL reflector height timeseries files

**Example:**

    from midgard import parsers
    p = parsers.parse_file(parser_name='gnssrefl_allrh', file_path='tgde_allRH.txt')
    data = p.as_dict()

**Description:**

Reads data from files in GNSSREFL reflector height timeseries files



### **GnssreflAllRh**

Full name: `midgard.parsers.gnssrefl_allrh.GnssreflAllRh`

Signature: `(file_path: Union[str, pathlib.Path], encoding: Optional[str] = None) -> None`

A parser for reading GNSSREFL reflector height timeseries files

Following **data** are available after reading Terrapos residual file:

| Parameter                 | Description                                                                     |
|---------------------------|---------------------------------------------------------------------------------|
| amplitude                 | Amplitude                                                                       |
| azimuth                   | Azimuth in [deg]                                                                |
| frequency                 | GNSS frequency identifier                                                       |
| peak2noise                | Peak to noise                                                                   |
| reflection_height         | Reflection height in [m]                                                        |
| satellite                 | Satellite number                                                                |
| time                      | Time as datetime object                                                         |

and **meta**-data:

| Key                  | Description                                                                          |
|----------------------|--------------------------------------------------------------------------------------|
| \__data_path__       | File path                                                                            |
| \__parser_name__     | Parser name                                                                          |



## midgard.parsers.gravsoft_grid
A parser for reading GRAVSOFT grid text files

**Description:**
GRAVSOFT grid data are stored rowwise from north to south. The grid values are initiated with label of latitude (lat) and longitude (lon) limits and spacing followed by the data section like:

    lat1 lat2 lon1 lon2 dlat dlon
 
    dn1  dn2 ... dnm
    ...
    ...
    d11  d12 ... d1m 
 
The grid label defines the exact latitude and longitude of the grid points with:

    lat1: west boundary of latitude
    lat2: east boundary of latitude
    lon1: west boundary of longitude
    lon2: east boundary of longitude
    dlat: latitude grid spacing
    dlon: longitude grid spacing
    
The first data value in a grid file is thus the NW-corner (lat2, lon1) and the last the SE-corner (lat1, lon2). The number of points in a grid file is thus:

    num_lat = (lat2 - lat1)/dlat + 1
    num_lon = (lon2 - lon1)/dlon + 1
    
Unknown data are shown by 9999.

More information about the GRAVSOFT grid format can be found under:

Forsberg, R. and Tscherning, C. C. (2014): "An overview manual for the GRAVSOFT Geodetic Gravity Field Modelling 
Programs", 3. edition, August 2014

**Example:**

    from midgard import parsers

    p = parsers.parse_file(parser_name="gravsoft_grid",  file_path="MeanSeaLevel1996-2014_above_Ellipsoid_EUREF89_v2021a.bin")
    data = p.as_dict()
    



### **GravsoftGrid**

Full name: `midgard.parsers.gravsoft_grid.GravsoftGrid`

Signature: `(file_path: Union[str, pathlib.Path], encoding: Optional[str] = None) -> None`

A parser for reading GRAVSOFT grid text files

Following **data** are available after reading data:

| Parameter           | Description                                                                           |
|---------------------|---------------------------------------------------------------------------------------|
| griddata            | Grid data with ordered grid blocks as list                                            |

and **meta**-data:

| Key                 | Description                                                                           |
|---------------------|---------------------------------------------------------------------------------------|
| grid_increment_lat  | Latitude grid increment in degree                                                     |
| grid_increment_lon  | Longitude grid increment in degree                                                    |
| grid_lat_max        | Maximal latitude border limit of grid area in degree                                  |
| grid_lat_max        | Maximal latitude border limit of grid area in degree                                  |
| grid_lat_min        | Minimal latitude border limit of grid area in degree                                  |
| grid_lon_max        | Maximal longitude border limit of grid area in degree                                 |
| grid_lon_min        | Minimal longitude border limit of grid area in degree                                 |
| __data_path__       | File path                                                                             |
| __parser_name__     | Parser name                                                                           |


## midgard.parsers.rinex212_nav
A parser for reading GNSS RINEX navigation file (exception GLONASS and SBAS)

**Example:**
    from midgard import parsers

    # Parse data
    parser = parsers.parse_file(parser_name="rinex212_nav", file_path=file_path)

    # Get Dataset with parsed data
    dset = parser.as_dataset()


**Description:**

Reads GNSS data from files in the RINEX navigation file format 2.12 (see :cite:`rinex2`). An exception is, that this
parser does not handle GLONASS and SBAS navigation messages. All navigation time epochs (time of clock (toc)) are
converted to GPS time scale.

The navigation message is not defined for GALILEO, BeiDou, QZSS and IRNSS in RINEX format 2.12. In this case the RINEX
3.03 definition is used (see :cite:`rinex3`).



### **Rinex212NavParser**

Full name: `midgard.parsers.rinex212_nav.Rinex212NavParser`

Signature: `(*args: Tuple[Any], **kwargs: Dict[Any, Any])`

A parser for reading RINEX navigation file

The parser reads GNSS broadcast ephemeris in RINEX format 2.12 (see :cite:`rinex2`).

#TODO: Would it not be better to use one leading underscore for non-public methods and instance variables.

**Attributes:**

data (Dict):                  The (observation) data read from file.
data_available (Boolean):     Indicator of whether data are available.
file_encoding (String):       Encoding of the datafile.
file_path (Path):             Path to the datafile that will be read.
meta (Dict):                  Metainformation read from file.
parser_name (String):         Name of the parser (as needed to call parsers.parse_...).        
system (String):              GNSS identifier.

Methods:
    as_dataframe()                Return the parsed data as a Pandas DataFrame
    as_dataset()                  Return the parsed data as a Midgard Dataset
    as_dict()                     Return the parsed data as a dictionary
    parse()                       Parse data
    parse_line()                  Parse line
    postprocess_data()            Do simple manipulations on the data after they are read
    read_data()                   Read data from the data file
    setup_parser()                Set up information needed for the parser
    setup_postprocessors()        List postprocessors that should be called after parsing

    _check_nav_message()          Check correctness of navigation message
    _get_system_from_file_extension()  Get GNSS by reading RINEX navigation file extension
    _parse_file()                 Read a data file and parse the content
    _parse_ionospheric_corr()     Parse entries of RINEX header `IONOSPHERIC CORR` to instance variable `meta`.
    _parse_leap_seconds()         Parse entries of RINEX header `LEAP SECONDS` to instance variable `meta`.
    _parse_obs_float()            Parse float entries of RINEX navigation data block to instance variable 'data'.
    _parse_observation_epoch()    Parse observation epoch information of RINEX navigation data record
    _parse_string()               Parse string entries of SP3 header to instance variable 'meta'
    _parse_string_list()          Parse string entries of RINEX header to instance variable 'meta' in a list
    _parse_time_system_corr()     Parse entries of RINEX header `TIME SYSTEM CORR` to instance variable `meta`.
    _rename_fields_based_on_system()  Rename general GNSS fields to GNSS specific ones
    _time_system_correction()     Apply correction to given time system for getting GPS time scale


### SYSNAMES (dict)
`SYSNAMES = {'gnss_data_info': {'G': 'codes_l2', 'J': 'codes_l2', 'E': 'data_source'}, 'gnss_interval': {'G': 'fit_interval', 'J': 'fit_interval', 'C': 'age_of_clock_corr'}, 'gnss_iodc_groupdelay': {'G': 'iodc', 'J': 'iodc', 'E': 'bgd_e1_e5b', 'C': 'tgd_b2_b3'}, 'gnss_l2p_flag': {'G': 'l2p_flag', 'J': 'l2p_flag'}, 'gnss_tgd_bgd': {'G': 'tgd', 'J': 'tgd', 'E': 'bgd_e1_e5a', 'C': 'tgd_b1_b3', 'I': 'tgd'}}`


### SYSTEM_FILE_EXTENSION (dict)
`SYSTEM_FILE_EXTENSION = {'n': 'G', 'g': 'R', 'l': 'E'}`


### SYSTEM_TIME_OFFSET_TO_GPS_SECOND (dict)
`SYSTEM_TIME_OFFSET_TO_GPS_SECOND = {'C': 14, 'E': 0, 'I': 0, 'J': 0}`


### SYSTEM_TIME_OFFSET_TO_GPS_WEEK (dict)
`SYSTEM_TIME_OFFSET_TO_GPS_WEEK = {'C': 1356, 'E': 0, 'I': 0, 'J': 0}`


## midgard.parsers.rinex2_nav
A parser for reading GNSS RINEX navigation file (exception GLONASS and SBAS)

**Example:**
    from midgard import parsers

    # Parse data
    parser = parsers.parse_file(parser_name="rinex2_nav", file_path=file_path)

    # Get Dataset with parsed data
    dset = parser.as_dataset()


**Description:**

Reads GNSS data from files in the RINEX navigation file format 2.11 (see :cite:`rinex2`). An exception is, that this
parser does not handle GLONASS and SBAS navigation messages. All navigation time epochs (time of clock (toc)) are
converted to GPS time scale.

The navigation message is not defined for GALILEO, BeiDou, QZSS and IRNSS in RINEX format 2.11. In this case the RINEX
3.03 definition is used (see :cite:`rinex3`).



### **Rinex2NavParser**

Full name: `midgard.parsers.rinex2_nav.Rinex2NavParser`

Signature: `(*args: Tuple[Any], **kwargs: Dict[Any, Any])`

A parser for reading RINEX navigation file

The parser reads GNSS broadcast ephemeris in RINEX format 2.11 (see :cite:`rinex2`).

#TODO: Would it not be better to use one leading underscore for non-public methods and instance variables.

**Attributes:**

data (Dict):                  The (observation) data read from file.
data_available (Boolean):     Indicator of whether data are available.
file_encoding (String):       Encoding of the datafile.
file_path (Path):             Path to the datafile that will be read.
meta (Dict):                  Metainformation read from file.
parser_name (String):         Name of the parser (as needed to call parsers.parse_...).        
system (String):              GNSS identifier.

Methods:
    as_dataframe()                Return the parsed data as a Pandas DataFrame
    as_dataset()                  Return the parsed data as a Midgard Dataset
    as_dict()                     Return the parsed data as a dictionary
    parse()                       Parse data
    parse_line()                  Parse line
    postprocess_data()            Do simple manipulations on the data after they are read
    read_data()                   Read data from the data file
    setup_parser()                Set up information needed for the parser
    setup_postprocessors()        List postprocessors that should be called after parsing

    _check_nav_message()          Check correctness of navigation message
    _get_system_from_file_extension()  Get GNSS by reading RINEX navigation file extension
    _parse_file()                 Read a data file and parse the content
    _parse_ion_alpha()            Parse entries of RINEX header `ION ALPHA` to instance variable `meta`.
    _parse_ion_beta()             Parse entries of RINEX header `ION BETA` to instance variable `meta`.
    _parse_obs_float()            Parse float entries of RINEX navigation data block to instance variable 'data'.
    _parse_observation_epoch()    Parse observation epoch information of RINEX navigation data record
    _parse_string()               Parse string entries of SP3 header to instance variable 'meta'
    _parse_string_list()          Parse string entries of RINEX header to instance variable 'meta' in a list
    _parse_time_system_corr()     Parse entries of RINEX header `DELTA-UTC: A0,A1,T,W` to instance variable `meta`.
    _rename_fields_based_on_system()  Rename general GNSS fields to GNSS specific ones
    _time_system_correction()     Apply correction to given time system for getting GPS time scale


### SYSNAMES (dict)
`SYSNAMES = {'gnss_data_info': {'G': 'codes_l2', 'J': 'codes_l2', 'E': 'data_source'}, 'gnss_interval': {'G': 'fit_interval', 'J': 'fit_interval', 'C': 'age_of_clock_corr'}, 'gnss_iodc_groupdelay': {'G': 'iodc', 'J': 'iodc', 'E': 'bgd_e1_e5b', 'C': 'tgd_b2_b3'}, 'gnss_l2p_flag': {'G': 'l2p_flag', 'J': 'l2p_flag'}, 'gnss_tgd_bgd': {'G': 'tgd', 'J': 'tgd', 'E': 'bgd_e1_e5a', 'C': 'tgd_b1_b3', 'I': 'tgd'}}`


### SYSTEM_FILE_EXTENSION (dict)
`SYSTEM_FILE_EXTENSION = {'n': 'G', 'g': 'R', 'l': 'E'}`


### SYSTEM_TIME_OFFSET_TO_GPS_SECOND (dict)
`SYSTEM_TIME_OFFSET_TO_GPS_SECOND = {'C': 14, 'E': 0, 'I': 0, 'J': 0}`


### SYSTEM_TIME_OFFSET_TO_GPS_WEEK (dict)
`SYSTEM_TIME_OFFSET_TO_GPS_WEEK = {'C': 1356, 'E': 0, 'I': 0, 'J': 0}`


## midgard.parsers.rinex2_obs
A parser for reading Rinex data

**Example:**

    from midgard import parsers
    
    # Parse data
    parser = parsers.parse_file(parser_name="rinex2_obs", file_path=file_path)
    
    # Get Dataset with parsed data
    dset = parser.as_dataset()

**Description:**

Reads data from files in the Rinex file format 2.11 (see :cite:`rinex2`).



### **Rinex2Parser**

Full name: `midgard.parsers.rinex2_obs.Rinex2Parser`

Signature: `(*args: Tuple[Any], sampling_rate: Optional[float] = None, convert_unit: bool = False, **kwargs: Dict[Any, Any]) -> None`

A parser for reading RINEX observation file

The parser reads GNSS observations in RINEX format 2.11 (see :cite:`rinex2`). The GNSS observations
are sampled after sampling rate definition in configuration file.

**Attributes:**

convert_unit (Boolean):       Convert unit from carrier-phase and Doppler observation to meter. Exception:
                                  unit conversion for GLONASS observations is not implemented.
data (Dict):                  The (observation) data read from file.
data_available (Boolean):     Indicator of whether data are available.
file_encoding (String):       Encoding of the datafile.
file_path (Path):             Path to the datafile that will be read.
meta (Dict):                  Metainformation read from file.
parser_name (String):         Name of the parser (as needed to call parsers.parse_...).
sampling_rate (Float):        Sampling rate in seconds.
system (String):              GNSS identifier.
time_scale (String):          Time scale, which is used to define the time scale of Dataset. GPS time scale is
                                  used. If another time scale is given e.g. BDT, then the time entries are 
                                  converted to GPS time scale. An exception is if GLONASS time scale is given, 
                                  then UTC is used as time scale. Hereby should be noted, the reported GLONASS time
                                  has the same hours as UTC and not UTC+3 h as the original GLONASS System Time in
                                  the RINEX file definition.


### SYSTEM_TIME_OFFSET_TO_GPS_TIME (dict)
`SYSTEM_TIME_OFFSET_TO_GPS_TIME = {'BDT': 14, 'GAL': 0, 'IRN': 0, 'QZS': 0}`


## midgard.parsers.rinex3_nav
A parser for reading GNSS RINEX v3.03 navigation file (exception GLONASS and SBAS)

**Example:**

    from midgard import parsers

    # Parse data
    parser = parsers.parse_file(parser_name="rinex3_nav", file_path=file_path)

    # Get Dataset with parsed data
    dset = parser.as_dataset()

**Description:**

Reads GNSS data from files in the RINEX navigation file format 3.03 (see :cite:`rinex3`). An exception is also, that
this parser does not handle GLONASS and SBAS navigation messages. All navigation time epochs (time of clock (toc)) are
converted to GPS time scale.



### **Rinex3NavParser**

Full name: `midgard.parsers.rinex3_nav.Rinex3NavParser`

Signature: `(file_path: Union[str, pathlib.Path], encoding: Optional[str] = None) -> None`

A parser for reading RINEX navigation file

The parser reads GNSS broadcast ephemeris in RINEX format 3.03 (see :cite:`rinex3`) except for GLONASS and SBAS.

#TODO: Would it not be better to use one leading underscore for non-public methods and instance variables.

**Attributes:**

data (Dict):                  The (observation) data read from file.
data_available (Boolean):     Indicator of whether data are available.
file_encoding (String):       Encoding of the datafile.
file_path (Path):             Path to the datafile that will be read.
meta (Dict):                  Metainformation read from file.
parser_name (String):         Name of the parser (as needed to call parsers.parse_...).        
system (String):              GNSS identifier.

Methods:
    as_dataframe()                Return the parsed data as a Pandas DataFrame
    as_dataset()                  Return the parsed data as a Midgard Dataset
    as_dict()                     Return the parsed data as a dictionary
    parse()                       Parse data
    parse_line()                  Parse line
    postprocess_data()            Do simple manipulations on the data after they are read
    read_data()                   Read data from the data file
    setup_parser()                Set up information needed for the parser
    setup_postprocessors()        List postprocessors that should be called after parsing

    _check_nav_message()          Check correctness of navigation message
    _parse_file()                 Read a data file and parse the content
    _parse_ionospheric_corr()     Parse entries of RINEX header `IONOSPHERIC CORR` to instance variable `meta`.
    _parse_leap_seconds()         Parse entries of RINEX header `LEAP SECONDS` to instance variable `meta`.
    _parse_obs_float()            Parse float entries of RINEX navigation data block to instance variable 'data'.
    _parse_observation_epoch()    Parse observation epoch information of RINEX navigation data record
    _parse_string()               Parse string entries of SP3 header to instance variable 'meta'
    _parse_string_list()          Parse string entries of RINEX header to instance variable 'meta' in a list
    _parse_time_system_corr()     Parse entries of RINEX header `TIME SYSTEM CORR` to instance variable `meta`.
    _rename_fields_based_on_system()  Rename general GNSS fields to GNSS specific ones
    _time_system_correction()     Apply correction to given time system for getting GPS time scale


### SYSNAMES (dict)
`SYSNAMES = {'gnss_data_info': {'G': 'codes_l2', 'J': 'codes_l2', 'E': 'data_source'}, 'gnss_interval': {'G': 'fit_interval', 'J': 'fit_interval', 'C': 'age_of_clock_corr'}, 'gnss_iodc_groupdelay': {'G': 'iodc', 'J': 'iodc', 'E': 'bgd_e1_e5b', 'C': 'tgd_b2_b3'}, 'gnss_l2p_flag': {'G': 'l2p_flag', 'J': 'l2p_flag'}, 'gnss_tgd_bgd': {'G': 'tgd', 'J': 'tgd', 'E': 'bgd_e1_e5a', 'C': 'tgd_b1_b3', 'I': 'tgd'}}`


### SYSTEM_TIME_OFFSET_TO_GPS_SECOND (dict)
`SYSTEM_TIME_OFFSET_TO_GPS_SECOND = {'C': 14, 'E': 0, 'G': 0, 'I': 0, 'J': 0}`


### SYSTEM_TIME_OFFSET_TO_GPS_WEEK (dict)
`SYSTEM_TIME_OFFSET_TO_GPS_WEEK = {'C': 1356, 'E': 0, 'G': 0, 'I': 0, 'J': 0}`


## midgard.parsers.rinex3_obs
A parser for reading RINEX format 3.03 data

**Example:**

    from midgard import parsers
    
    # Parse data
    parser = parsers.parse_file(parser_name="rinex3_obs", file_path=file_path)
      
    # Get Dataset with parsed data
    dset = parser.as_dataset()

**Description:**

Reads data from files in the RINEX file format version 3.03 (see :cite:`rinex3`).




### **Rinex3Parser**

Full name: `midgard.parsers.rinex3_obs.Rinex3Parser`

Signature: `(*args: Tuple[Any], sampling_rate: Optional[float] = None, convert_unit: bool = False, **kwargs: Dict[Any, Any]) -> None`

A parser for reading RINEX observation file

The parser reads GNSS observations in RINEX format 3.03 (see :cite:`rinex3`). The GNSS observations
are sampled after sampling rate definition in configuration file.

**Attributes:**

convert_unit (Boolean):       Convert unit from carrier-phase and Doppler observation to meter. Exception:
                                  unit conversion for GLONASS observations is not implemented.
data (Dict):                  The (observation) data read from file.
data_available (Boolean):     Indicator of whether data are available.
file_encoding (String):       Encoding of the datafile.
file_path (Path):             Path to the datafile that will be read.
meta (Dict):                  Metainformation read from file.
parser_name (String):         Name of the parser (as needed to call parsers.parse_...).
sampling_rate (Float):        Sampling rate in seconds.
time_scale (String):          Time scale, which is used to define the time scale of Dataset. GPS time scale is
                                  used. If another time scale is given e.g. BDT, then the time entries are 
                                  converted to GPS time scale. An exception is if GLONASS time scale is given, 
                                  then UTC is used as time scale. Hereby should be noted, the reported GLONASS time
                                  has the same hours as UTC and not UTC+3 h as the original GLONASS System Time in
                                  the RINEX file definition.
system (String):              GNSS identifier.


### SYSTEM_TIME_OFFSET_TO_GPS_TIME (dict)
`SYSTEM_TIME_OFFSET_TO_GPS_TIME = {'BDT': 14, 'GAL': 0, 'IRN': 0, 'QZS': 0}`


## midgard.parsers.rinex_nav
A parser for reading GNSS RINEX navigation files

**Example:**

    from midgard.data import dataset
    from midgard import parsers

    # Parse data
    parser = parsers.parse(file_path=file_path)

    # Create a empty Dataset
    dset = data.Dataset()

    # Fill Dataset with parsed data
    parser.write_to_dataset(dset)


**Description:**

Reads GNSS ephemeris data from RINEX navigation file in format 2.11 (see :cite:`rinex2`) or 3.03 (see :cite:`rinex3`).



### **get_rinex2_or_rinex3**()

Full name: `midgard.parsers.rinex_nav.get_rinex2_or_rinex3`

Signature: `(file_path: pathlib.PosixPath) -> 'TODO'`

Use either Rinex2NavParser or Rinex3NavParser for reading orbit files in format 2.11 or 3.03.

Firstly the RINEX file version is read. Based on the read version number it is decided, which Parser should be
used.

**Args:**

file_path (pathlib.PosixPath):  File path to broadcast orbit file.


## midgard.parsers.sinex_discontinuities
A parser for reading data from discontinuities.snx in SINEX format

**Example:**

    from midgard import parsers
    p = parsers.parse_file(parser_name='discontinuities_snx', file_path='discontinuities_snx')
    data = p.as_dict()

**Description:**

Reads discontinuities of GNSS station timeseries in SINEX format .




### **DiscontinuitiesSnxParser**

Full name: `midgard.parsers.sinex_discontinuities.DiscontinuitiesSnxParser`

Signature: `(file_path: Union[str, pathlib.Path], encoding: Optional[str] = None, header: bool = True) -> None`

A parser for reading data from discontinuties.snx file in SINEX format

The solution discontinuity dictionary has as keys the site identifiers and as value the 'solution_discontinuity'
entry. The dictionary has following strucuture:

   self.data[site] = { 'solution_discontinuity':  [] }   # SOLUTION/DISCONTINUITY SINEX block information

with the 'solution_discontinuity' dictionary entries

   solution_discontinuity[ii]     = [ 'point_code':         point_code,
                                      'soln':               soln,
                                      'obs_code':           obs_code,
                                      'start_time':         start_time,
                                      'end_time':           end_time,
                                      'event_code':         event_code,
                                      'description':        description ]

The counter 'ii' ranges from 0 to n and depends on how many discontinuities exists for a site. Note also, that 
time entries (e.g. start_time, end_time) are given as 'datetime'. If the time is defined as 00:000:00000 in the
SINEX file, then the value is saved as 'None' in the Sinex class.


## midgard.parsers.sinex_events
A parser for reading data from events.snx in SINEX format

**Example:**

    from midgard import parsers
    p = parsers.parse_file(parser_name='events_snx', file_path='events_snx')
    data = p.as_dict()

**Description:**

Reads events related to GNSS configuration, environment changes or station timeseries data problems in SINEX format .




### **EventsSnxParser**

Full name: `midgard.parsers.sinex_events.EventsSnxParser`

Signature: `(file_path: Union[str, pathlib.Path], encoding: Optional[str] = None, header: bool = True) -> None`

A parser for reading data from events.snx file in SINEX format

The solution events dictionary has as keys the site identifiers and as value the 'solution_event'
entry. The dictionary has following strucuture:

   self.data[site] = { 'solution_event':  [] }   # SOLUTION/EVENT SINEX block information

with the 'solution_event' dictionary entries

   solution_event[ii]    = [ 'point_code':         point_code,
                             'soln':               soln,
                             'obs_code':           obs_code,
                             'start_time':         start_time,
                             'end_time':           end_time,
                             'event_code':         event_code,
                             'description':        description ]

The counter 'ii' ranges from 0 to n and depends on how many events exists for a site. Note also, that 
time entries (e.g. start_time, end_time) are given as 'datetime'. If the time is defined as 00:000:00000 in the
SINEX file, then the value is saved as 'None' in the Sinex class.


## midgard.parsers.sinex_site
A parser for reading site related information from SINEX format

**Example:**

    from midgard import parsers
    p = parsers.parse_file(parser_name='sinex_site', file_path='sinex_site')
    data = p.as_dict()

**Description:**

Reads station related information (e.g. approximated station coordinates, receiver and antenna type, station 
eccentricities, ...) from files in SINEX format. Following blocks are read:

            FILE/COMMENT   
            SITE/ID
            SITE/RECEIVER
            SITE/ANTENNA
            SITE/ECCENTRICITY
            SOLUTION/EPOCHS
            SOLUTION/ESTIMATE

Note, that FILE/COMMENT block is only used for reading reference frame information ('ref_frame'), which is added to 
SOLUTION/ESTIMATE dictionary.



### **SinexSiteParser**

Full name: `midgard.parsers.sinex_site.SinexSiteParser`

Signature: `(file_path: Union[str, pathlib.Path], encoding: Optional[str] = None, header: bool = True) -> None`

A parser for reading site related information from SINEX format

site - Site dictionary, whereby keys are the site identifiers and values are a site entry
       dictionary with the keys 'site_antenna', 'site_eccentricity', 'site_id', 'site_receiver',
       'solution_epoch' and 'solution_estimate'. The site dictionary has following structure:

          self.site[site] = { 'site_antenna':          [],  # SITE/ANTENNA SINEX block information
                              'site_eccentricity':     [],  # SITE/ECCENTRICITY block information
                              'site_id':               {},  # SITE/ID block information
                              'site_receiver':         [],  # SITE/RECEIVER block information
                              'solution_epoch':        [],  # SOLUTION/EPOCH block information
                              'solution_estimate':     [],  # SOLUTION/ESTIMATE block information
          }

       with the site entry dictionary entries

          site_antenna[ii]      = { 'site_code':          site_code,
                                    'point_code':         point_code,
                                    'soln':               soln,
                                    'obs_code':           obs_code,
                                    'start_time':         start_time,
                                    'end_time':           end_time,
                                    'antenna_type':       antenna_type,
                                    'radome_type':        radome_type,
                                    'serial_number':      serial_number }

          site_eccentricity[ii] = { 'site_code':          site_code,
                                    'point_code':         point_code,
                                    'soln':               soln,
                                    'obs_code':           obs_code,
                                    'start_time':         start_time,
                                    'end_time':           end_time,
                                    'vector_1':           vector_1,
                                    'vector_2':           vector_2,
                                    'vector_3':           vector_3,
                                    'vector_type':        UNE }

          site_id               = { 'site_code':          site_code,
                                    'point_code':         point_code,
                                    'domes':              domes,
                                    'marker':             marker,
                                    'obs_code':           obs_code,
                                    'description':        description,
                                    'approx_lon':         approx_lon,
                                    'approx_lat':         approx_lat,
                                    'approx_height':      approx_height }

          site_receiver[ii]     = { 'site_code':          site_code,
                                    'point_code':         point_code,
                                    'soln':               soln,
                                    'obs_code':           obs_code,
                                    'start_time':         start_time,
                                    'end_time':           end_time,
                                    'receiver_type':      receiver_type,
                                    'serial_number':      serial_number,
                                    'firmware':           firmware }

          solution_epochs[ii]   = { 'site_code':          site_code,
                                    'point_code':         point_code,
                                    'soln':               soln,
                                    'obs_code':           obs_code,
                                    'start_epoch':        start_epoch,
                                    'end_epoch':          end_epoch,
                                    'mean_epoch':         mean_epoch }

          solution_estimate[ii] = { 'param_idx':          param_idx,
                                    'param_name':         param_name,
                                    'point_code':         point_code,
                                    'site_code':          site_code,
                                    'soln':               soln,
                                    'ref_epoch':          ref_epoch,
                                    'unit':               unit,
                                    'constraint':         constraint,
                                    'estimate':           estimate,
                                    'estimate_std':       estimate_std,
                                    'ref_frame':          ref_frame }  # Note: ref_frame taken from
                                                                       #   FILE/COMMENT block, if exists.

       The counter 'ii' ranges from 0 to n and depends on how many antenna type, receiver type,
       antenna monument and station coordinate changes were done at each site. If the time is defined as
       00:000:00000 in the SINEX file, then the value is saved as 'None' in the Sinex class.



## midgard.parsers.sinex_tro
A parser for reading troposphere results in SNX format

**Description:**

The implementation is based on example output files from Bernese. The SINEX_TRO format is an extension of the regular
SINEX format, but mostly uses custom blocks. The following blocks are found in the example file:
+FILE/REFERENCE           (defined in SINEX 2.02)                                                      
+TROP/DESCRIPTION         (custom block)
+TROP/STA_COORDINATES     (custom block)
+TROP/SOLUTION            (custom block)

The format of the custom blocks are derived by reading example files and blocks defined in the format that is not 
present in the example files are not implemented yet.

Format description: https://files.igs.org/pub/data/format/sinex_tropo.txt



### **BernTropSnxParser**

Full name: `midgard.parsers.sinex_tro.BernTropSnxParser`

Signature: `(file_path, encoding=None)`

A parser for reading data from Bernese troposphere files in SNX format


## midgard.parsers.slr_prediction
A parser for reading SLR prediction files

**Description:**

Reads data from files in the CPF file format as defined in http://ilrs.gsfc.nasa.gov/docs/2006/cpf_1.01.pdf



### **SlrPredictionParser**

Full name: `midgard.parsers.slr_prediction.SlrPredictionParser`

Signature: `(file_path: Union[str, pathlib.Path], encoding: Optional[str] = None) -> None`

A parser for reading SLR prediction files (CPF format)


## midgard.parsers.spring_csv
A parser for reading Spring CSV output files

**Example:**

    from midgard import parsers
    p = parsers.parse_file(parser_name='spring_csv', file_path='ADOP20473_0000.csv')
    data = p.as_dict()

**Description:**

Reads data from files in Spring CSV output format. The header information of the Spring CSV file is not read (TODO).


### **SpringCsvParser**

Full name: `midgard.parsers.spring_csv.SpringCsvParser`

Signature: `(file_path: Union[str, pathlib.Path], encoding: Optional[str] = None) -> None`

A parser for reading Spring CSV output files

The Spring CSV data header line is used to define the keys of the **data** dictionary. The values of the **data** 
dictionary are represented by the Spring CSV colum values.

Depending on the Spring CSV following dataset fields can be available:

| Field               | Description                                                                           |
|---------------------|---------------------------------------------------------------------------------------|
| acquiredsat         | Number of acquired satellites (TODO?)                                                 |
| gdop                | Geometric dilution of precision                                                       |
| hdop                | Horizontal dilution of precision                                                      |
| pdop                | Position (3D) dilution of precision                                                   |
| satinview           | Number of satellites in view                                                          |
| system              | GNSS identifier based on RINEX definition (e.g. G: GPS, E: Galileo)                   |
| tdop                | Time dilution of precision                                                            |
| time                | Observation time given as Time object                                                 |
| usedsat             | Number of used satellites                                                             |
| vdop                | Vertical dilution of precision                                                        |
| ...                 | ...                                                                                   |


## midgard.parsers.ssc_site
A parser for reading data from TRF files in SSC format


**Example:**

    from midgard import parsers
    p = parsers.parse_file(parser_name='ssc_site', file_path='ssc_site')
    data = p.as_dict()

**Description:**

Reads station positions and velocities from TRF files in SSC format. The velocity model is a simple linear offset
based on the reference epoch.



### **SscSiteParser**

Full name: `midgard.parsers.ssc_site.SscSiteParser`

Signature: `(file_path: Union[str, pathlib.Path], encoding: Optional[str] = None) -> None`

A parser for reading data from TRF files in SSC format


## midgard.parsers.terrapos_position
A parser for reading Terrapos position output file

**Example:**

    from midgard import parsers
    p = parsers.parse_file(parser_name='terrapos_position', file_path='Gal_C1X_brdc_land_30sec_24hrs_FNAV-file.txt')
    data = p.as_dict()

**Description:**

Reads data from files in Terrapos position output format.



### **TerraposPositionParser**

Full name: `midgard.parsers.terrapos_position.TerraposPositionParser`

Signature: `(*args: Tuple[Any], station: Optional[str] = None, **kwargs: Dict[Any, Any]) -> None`

A parser for reading Terrapos position output file

Following **data** are available after reading Terrapos position file:

| Key                  | Description                                                                          |
|----------------------|--------------------------------------------------------------------------------------|
| gpsweek              | GPS week                                                                             |
| gpssec               | Seconds of GPS week                                                                  |
| head                 | Head in [deg]                                                                        |
| height               | Ellipsoidal height in [m]                                                            |
| lat                  | Latitude in [deg]                                                                    |
| lon                  | Longitude in [deg]                                                                   |
| num_sat              | Number of satellites                                                                 |
| pdop                 | Position Dilution of Precision (PDOP)                                                |
| pitch                | Pitch in [deg]                                                                       |
| reliability_east     | East position external reliability in [m] #TODO: Is that correct?                    |
| reliability_height   | Height position external reliability in [m] #TODO: Is that correct?                  |
| reliability_north    | North position external reliability in [m] #TODO: Is that correct?                   |
| roll                 | Roll in [deg]                                                                        |
| sigma_east           | Standard deviation of East position in [m] #TODO: Is that correct?                   |
| sigma_height         | Standard deviation of Height position in [m] #TODO: Is that correct?                 |
| sigma_north          | Standard deviation of North position in [m] #TODO: Is that correct?                  |

and **meta**-data:

| Key                  | Description                                                                          |
|----------------------|--------------------------------------------------------------------------------------|
| \__data_path__       | File path                                                                            |
| \__parser_name__     | Parser name                                                                          |


## midgard.parsers.terrapos_residual
A parser for reading Terrapos residual file

**Example:**

    from midgard import parsers
    p = parsers.parse_file(parser_name='terrapos_residual', file_path='PPP-residuals.txt')
    data = p.as_dict()

**Description:**

Reads data from files in Terrapos residual format.



### **TerraposResidualParser**

Full name: `midgard.parsers.terrapos_residual.TerraposResidualParser`

Signature: `(file_path: Union[str, pathlib.Path], encoding: Optional[str] = None) -> None`

A parser for reading Terrapos residual file

Following **data** are available after reading Terrapos residual file:

| Parameter           | Description                                                                           |
|---------------------|---------------------------------------------------------------------------------------|
| azimuth             | Azimuth of satellites in [deg]                                                        |
| elevation           | Elevation of satellites in [deg]                                                      |
| gpsweek             | GPS week                                                                              |
| gpssec              | Seconds of GPS week                                                                   |
| residual_code       | Code (pseudorange) residuals in [m]                                                   |
| residual_doppler    | Doppler residuals in [m]                                                              |
| residual_phase      | Carrier-phase residuals in [m]                                                        |
| satellite           | Satellite PRN number together with GNSS identifier (e.g. G07)                         |
| system              | GNSS identifier                                                                       |

and **meta**-data:

| Key                  | Description                                                                          |
|----------------------|--------------------------------------------------------------------------------------|
| \__data_path__       | File path                                                                            |
| \__parser_name__     | Parser name                                                                          |



## midgard.parsers.ure_control_tool_csv
A parser for reading URE Control Tool CSV output files

**Example:**

    from midgard import parsers
    p = parsers.parse_file(parser_name='ure_control_tool_csv', file_path='G_GAL258_E1E5a_URE-AllPRN_190301.csv')
    data = p.as_dict()

**Description:**

Reads data from files in URE Control Tool CSV output format. The header information of the URE Control Tool CSV file is
not read (TODO).


### **UreControlToolCsvParser**

Full name: `midgard.parsers.ure_control_tool_csv.UreControlToolCsvParser`

Signature: `(file_path: Union[str, pathlib.Path], encoding: Optional[str] = None) -> None`

A parser for reading URE Control Tool CSV output files

The URE Control Tool CSV data header line is used to define the keys of the **data** dictionary. The values of the 
**data** dictionary are represented by the URE Control Tool CSV colum values.



## midgard.parsers.vlbi_source_names
A parser for reading IVS source names translation table


### **VlbiSourceNamesParser**

Full name: `midgard.parsers.vlbi_source_names.VlbiSourceNamesParser`

Signature: `(file_path: Union[str, pathlib.Path], encoding: Optional[str] = None) -> None`

A parser for reading IVS source names translation table

See https://vlbi.gsfc.nasa.gov/output for an example of a IVS source name file


## midgard.parsers.wip_rinex
A parser for reading Rinex files


### **rinex**()

Full name: `midgard.parsers.wip_rinex.rinex`

Signature: `(**parser_args: Any) -> midgard.parsers._parser_rinex.RinexParser`

Dispatch to correct subclass based on Rinex file type

## midgard.parsers.wip_rinex2_nav
A parser for reading RINEX navigation files with version 2.xx


### **Rinex2NavParser**

Full name: `midgard.parsers.wip_rinex2_nav.Rinex2NavParser`

Signature: `(file_path: Union[str, pathlib.Path], encoding: Optional[str] = None, logger=<built-in function print>, sampling_rate: Optional[int] = None, strict: bool = False) -> None`

A parser for reading RINEX navigation files with version 2.xx



## midgard.parsers.wip_rinex2_nav_header
RINEX navigation header classes for file format version 2.xx


### **Rinex2NavHeaderMixin**

Full name: `midgard.parsers.wip_rinex2_nav_header.Rinex2NavHeaderMixin`

Signature: `()`

A mixin defining which RINEX navigation headers are mandatory and optional in RINEX version 2.xx

### **Rinex2NavHeaderParser**

Full name: `midgard.parsers.wip_rinex2_nav_header.Rinex2NavHeaderParser`

Signature: `(file_path: Union[str, pathlib.Path], encoding: Optional[str] = None, logger=<built-in function print>, sampling_rate: Optional[int] = None, strict: bool = False) -> None`

A parser for reading just the RINEX version 2.xx navigation header

The data in the rinex file will not be parsed.


## midgard.parsers.wip_rinex2_obs
A parser for reading RINEX observation files with version 2.xx


### **Rinex2ObsParser**

Full name: `midgard.parsers.wip_rinex2_obs.Rinex2ObsParser`

Signature: `(file_path: Union[str, pathlib.Path], encoding: Optional[str] = None, logger=<built-in function print>, sampling_rate: Optional[int] = None, strict: bool = False) -> None`

A parser for reading RINEX observation files with version 2.xx



## midgard.parsers.wip_rinex2_obs_header
RINEX observation header classes for file format version 3.xx


### **Rinex2ObsHeaderMixin**

Full name: `midgard.parsers.wip_rinex2_obs_header.Rinex2ObsHeaderMixin`

Signature: `()`

A mixin defining which RINEX observation headers are mandatory and optional in RINEX version 2.xx

### **Rinex2ObsHeaderParser**

Full name: `midgard.parsers.wip_rinex2_obs_header.Rinex2ObsHeaderParser`

Signature: `(file_path: Union[str, pathlib.Path], encoding: Optional[str] = None, logger=<built-in function print>, sampling_rate: Optional[int] = None, strict: bool = False) -> None`

A parser for reading just the RINEX version 2.xx observation header

The data in the rinex file will not be parsed.


## midgard.parsers.wip_rinex3_clk
A parser for reading RINEX clock files with version 3.xx


### **Rinex3ClkParser**

Full name: `midgard.parsers.wip_rinex3_clk.Rinex3ClkParser`

Signature: `(file_path: Union[str, pathlib.Path], encoding: Optional[str] = None, logger=<built-in function print>, sampling_rate: Optional[int] = None, strict: bool = False) -> None`

A parser for reading RINEX clock files with version 3.xx


## midgard.parsers.wip_rinex3_clk_header
RINEX clock header classes for file format version 3.xx


### **Rinex3ClkHeaderMixin**

Full name: `midgard.parsers.wip_rinex3_clk_header.Rinex3ClkHeaderMixin`

Signature: `()`

A mixin defining which RINEX clock headers are mandatory and optional in RINEX version 3.xx

### **Rinex3ClkHeaderParser**

Full name: `midgard.parsers.wip_rinex3_clk_header.Rinex3ClkHeaderParser`

Signature: `(file_path: Union[str, pathlib.Path], encoding: Optional[str] = None, logger=<built-in function print>, sampling_rate: Optional[int] = None, strict: bool = False) -> None`

A parser for reading just the RINEX version 3.xx clock header

The data in the rinex file will not be parsed.


## midgard.parsers.wip_rinex3_nav
A parser for reading RINEX navigation files with version 3.xx


### **Rinex3NavParser**

Full name: `midgard.parsers.wip_rinex3_nav.Rinex3NavParser`

Signature: `(file_path: Union[str, pathlib.Path], encoding: Optional[str] = None, logger=<built-in function print>, sampling_rate: Optional[int] = None, strict: bool = False) -> None`

A parser for reading RINEX navigation files with version 3.xx



## midgard.parsers.wip_rinex3_nav_header
RINEX navigation header classes for file format version 3.xx


### **Rinex3NavHeaderMixin**

Full name: `midgard.parsers.wip_rinex3_nav_header.Rinex3NavHeaderMixin`

Signature: `()`

A mixin defining which RINEX navigation headers are mandatory and optional in RINEX version 3.xx

### **Rinex3NavHeaderParser**

Full name: `midgard.parsers.wip_rinex3_nav_header.Rinex3NavHeaderParser`

Signature: `(file_path: Union[str, pathlib.Path], encoding: Optional[str] = None, logger=<built-in function print>, sampling_rate: Optional[int] = None, strict: bool = False) -> None`

A parser for reading just the RINEX version 3.xx navigation header

The data in the rinex file will not be parsed.


## midgard.parsers.wip_rinex3_obs
A parser for reading RINEX observation files with version 3.xx


### **Rinex3ObsParser**

Full name: `midgard.parsers.wip_rinex3_obs.Rinex3ObsParser`

Signature: `(file_path: Union[str, pathlib.Path], encoding: Optional[str] = None, logger=<built-in function print>, sampling_rate: Optional[int] = None, strict: bool = False) -> None`

A parser for reading RINEX observation files with version 3.xx



## midgard.parsers.wip_rinex3_obs_header
RINEX observation header classes for file format version 3.xx


### **Rinex3ObsHeaderMixin**

Full name: `midgard.parsers.wip_rinex3_obs_header.Rinex3ObsHeaderMixin`

Signature: `()`

A mixin defining which RINEX observation headers are mandatory and optional in RINEX version 3.xx

### **Rinex3ObsHeaderParser**

Full name: `midgard.parsers.wip_rinex3_obs_header.Rinex3ObsHeaderParser`

Signature: `(file_path: Union[str, pathlib.Path], encoding: Optional[str] = None, logger=<built-in function print>, sampling_rate: Optional[int] = None, strict: bool = False) -> None`

A parser for reading just the RINEX version 3.xx observation header

The data in the rinex file will not be parsed.


## midgard.parsers.wip_rinex_clk
A parser for reading Rinex navigation files


### **RinexClkParser**

Full name: `midgard.parsers.wip_rinex_clk.RinexClkParser`

Signature: `(file_path: Union[str, pathlib.Path], encoding: Optional[str] = None, logger=<built-in function print>, sampling_rate: Optional[int] = None, strict: bool = False) -> None`

Class for defining common methods for RINEX clock parsers.


### **rinex_clk**()

Full name: `midgard.parsers.wip_rinex_clk.rinex_clk`

Signature: `(**parser_args: Any) -> midgard.parsers._parser_rinex.RinexParser`

Dispatch to correct subclass based on version in Rinex file

## midgard.parsers.wip_rinex_nav
A parser for reading Rinex navigation files


### **RinexNavParser**

Full name: `midgard.parsers.wip_rinex_nav.RinexNavParser`

Signature: `(file_path: Union[str, pathlib.Path], encoding: Optional[str] = None, logger=<built-in function print>, sampling_rate: Optional[int] = None, strict: bool = False) -> None`

Class for defining common methods for RINEX navigation parsers.


### **rinex_nav**()

Full name: `midgard.parsers.wip_rinex_nav.rinex_nav`

Signature: `(**parser_args: Any) -> midgard.parsers._parser_rinex.RinexParser`

Dispatch to correct subclass based on version in Rinex file

## midgard.parsers.wip_rinex_obs
A parser for reading Rinex observation files


### **RinexObsParser**

Full name: `midgard.parsers.wip_rinex_obs.RinexObsParser`

Signature: `(file_path: Union[str, pathlib.Path], encoding: Optional[str] = None, logger=<built-in function print>, sampling_rate: Optional[int] = None, strict: bool = False) -> None`

Class for defining common methods for RINEX observation parsers.


### **rinex_obs**()

Full name: `midgard.parsers.wip_rinex_obs.rinex_obs`

Signature: `(**parser_args: Any) -> midgard.parsers._parser_rinex.RinexParser`

Dispatch to correct subclass based on version in Rinex file