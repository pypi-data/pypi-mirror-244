"""Receiver information classes

Description:
------------
This module is divided into three different types of classes:

    1. Main class Receiver provides basic functionality to the user. See examples.
    2. Receiver source type classes:
        - There is one class for each source type
        - A class with all relevant receiver information for a point in time.
    3. Receiver history source type classes:
        - There is one class for each source type
        - Converts input from source_data to a object of type ReceiverHistorySinex, etc and provides functions
          for accessing the history and relevant dates. 
        - The history consist of a time interval for which the entry is valid and an instance of a receiver 
          source type class for each defined time interval.

    If a source type does not contain information about the receiver the module will return 'None'.

Example:
--------
    
    from midgard import parsers
    from midgard.site_info.receiver import Receiver
    from datetime import datetime
    
    # Read SINEX data  
    p = parsers.parse_file(parser_name='sinex_site', file_path='./data/site_info/igs.snx')
    source_data = p.as_dict()
    all_stations = source_data.keys()
    
    # Get station information
    Receiver.get("snx", "osls", datetime(2020, 1, 1), source_data, source_path=p.file_path)
    Receiver.get("snx", all_stations, datetime(2020, 1, 1), source_data, source_path=p.file_path)
    
    Receiver.get_history("snx", "osls", source_data, source_path=p.file_path)
    Receiver.get_history("snx", all_stations, source_data, source_path=p.file_path)

"""

# Standard library imports
from collections import OrderedDict
from datetime import datetime
from typing import Any, Dict, List, Tuple, Union, Callable

# Midgard imports
from midgard.dev.exceptions import MissingDataError
from midgard.site_info.gnsseu.api import GnssEuApi
from midgard.site_info._site_info import SiteInfoBase, SiteInfoHistoryBase, ModuleBase
from midgard.site_info import convert_to_utc


class Receiver(ModuleBase):
    """Main class for converting receiver information from various sources into unified classes"""
    
    sources: Dict[str, Callable] = dict()


@Receiver.register_source
class ReceiverHistorySinex(SiteInfoHistoryBase):

    source: str = "snx"

    def _process_history(
                self, 
                source_data: Dict,
    ) -> Dict[Tuple[datetime, datetime], "ReceiverSinex"]:
        """Process receiver site history from SINEX file

        Args:
            source_data:  Source data with site information.

        Returns:
            Dictionary with (date_from, date_to) tuple as key. The values are ReceiverSinex objects.
        """

        if self.station in source_data:
            if "site_receiver" not in source_data[self.station]:
                raise MissingDataError(f"Station {self.station!r} is not given in SITE/RECEIVER SINEX block.")
            raw_info = source_data[self.station]["site_receiver"]
        elif self.station.upper() in source_data:
            if "site_receiver" not in source_data[self.station.upper()]:
                raise MissingDataError(f"Station {self.station.upper()!r} is not given in SITE/RECEIVER SINEX block.")
            raw_info = source_data[self.station.upper()]["site_receiver"]
        else:
            raise MissingDataError(f"Station {self.station!r} unknown in source '{self.source_path}'.")
        
        return self._create_history(self.station, raw_info)

    def _create_history(self, station: str, raw_info: List) -> Dict:
        """Create dictionary of antenna history for station
        """
        history = dict()
        for receiver_info in raw_info:
            receiver = ReceiverSinex(self.station, receiver_info)
            interval = (receiver.date_from, receiver.date_to)
            history[interval] = receiver

        return history


class ReceiverSinex(SiteInfoBase):
    """ Receiver class handling SINEX file receiver station information
    """

    source: str = "snx"
    fields: Dict[str, str] = dict(type="receiver_type", serial_number="serial_number", firmware="firmware")

    @property
    def date_from(self) -> datetime:
        """ Get receiver installation date from site information attribute

        Returns:
            Receiver installation date
        """
        if self._info["start_time"]:
            return self._info["start_time"]
        else:
            return datetime.min

    @property
    def date_to(self) -> datetime:
        """ Get receiver removing date from site information attribute

        Returns:
            Receiver removing date
        """
        if self._info["end_time"]:
            return self._info["end_time"]
        else:
            return datetime.max


@Receiver.register_source
class ReceiverHistorySsc(SiteInfoHistoryBase):

    source: str = "ssc"

    def _process_history(
                self, 
                source_data: Any = None,
    ) -> Union[None, Dict[Tuple[datetime, datetime], "ReceiverSinex"]]:
        """Process receiver site history from SINEX file

        Args:
            source_data:  Source data with site information.

        Returns:
            Dictionary with (date_from, date_to) tuple as key. The values are ReceiverSinex objects.
        """
        if self.station in source_data or self.station.upper() in source_data:
            # Station is defined but SSC files do not contain receiver information
            return None
        else:
            raise MissingDataError(f"Station {self.station!r} unknown in source '{self.source_path}'.")

@Receiver.register_source
class ReceiverHistoryGnssEu(SiteInfoHistoryBase):

    source = "gnsseu"

    def _process_history(self, source_data) -> Dict[Tuple[datetime, datetime], "ReceiverGnssEu"]:
        """Read receiver site history from gnssEu API

        Args:
            source_data:    api object for gnsseu

        Returns:
            Dictionary with (date_from, date_to) tuple as key. The values are ReceiverGnssEu objects.
        """
        # Get receiver history information
        if isinstance(source_data, GnssEuApi):
            # source_data is an Api object. Use api function to query database
            try:
                raw_info = source_data.get_sitelog(filter={"id": {"like": self.station}})
                if not raw_info:
                    raise MissingDataError(f"Station {self.station.upper()!r} unknown in source {self.source!r}.")
                if len(raw_info) > 1:
                    raise ValueError(f"Station {self.station.upper()!r} is not unique in source {self.source!r}. Use full station name.")
                station_data = raw_info[0]
            except ConnectionError as err:
                raise MissingDataError(f"Station {self.station.upper()!r} unknown in source {self.source!r}. Error: {err}")
        elif isinstance(source_data, dict):
            # source data is a dictionary. Use the keys to look up station data
            # This is a more efficient way to look up information when all data already has been queried from
            # the database through the api.get_sitelog_all function.
            sta = self.station.upper()
            try:
                raw_info = source_data[sta[0:4]]
                if len(raw_info) > 1:
                    if len(sta) == 9:
                        station_data = raw_info[sta]
                    else:
                        raise ValueError(f"Station {self.station.upper()!r} is not unique in source {self.source!r}. Use full station name.")
                else:
                    # Only one key in dictionary
                    station_data = raw_info[list(raw_info.keys())[0]]
            except KeyError:
                raise MissingDataError(f"Station {self.station.upper()!r} unknown in source {self.source!r}. Error: {err}")

        if not "sitelog" in station_data:
            raise MissingDataError(f"No sitelog information is available for station {self.station.upper()!r} in source {self.source!r}.")

        # Create list of receiver history
        history = OrderedDict()
        for receiver_info in station_data["sitelog"]["receivers"]:
            receiver = ReceiverGnssEu(self.station, receiver_info)
            interval = (receiver.date_from, receiver.date_to)
            history[interval] = receiver

        return history


class ReceiverGnssEu(SiteInfoBase):
    """ Receiver class handling gnssEu API receiver station information
    """

    source = "gnsseu"
    fields = dict(
        serial_number="serialNumber",
        firmware="firmwareVersion",
        elevation_mask="elevationCutoffVal",
    )

    @property
    def date_from(self) -> datetime:
        """ Get receiver installation date from gnssEu API site information attribute

        Returns:
            Receiver installation date
        """
        if self._info["dateInstalled"]:
            return convert_to_utc(datetime.fromisoformat(self._info["dateInstalled"]))
        else:
            return datetime.min

    @property
    def date_to(self) -> datetime:
        """ Get receiver removing date from gnssEu API site information attribute

        Returns:
            Receiver removing date
        """
        if self._info["dateRemoved"]:
            return convert_to_utc(datetime.fromisoformat(self._info["dateRemoved"]))
        else:
            return datetime.max

    @property
    def type(self) -> str:
        """ Get receiver type

        Returns:
            Receiver type
        """
        return self._info["receiverType"]
