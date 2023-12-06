"""
This module provides the classes BIDSTaskEvent, BIDSError, OnsetError, DurationError,
TrialTypeError, SampleError, ResponseTimeError, HedError, StimFileError, IdentifierError,
DatabaseError
"""

from typing import Union

from .bidsbehevent import BIDSBehEvent


class BIDSTaskEvent(BIDSBehEvent):
    """A class representing task events.

    This class describes timing and other properties of events recorded during a run. Events are,
    for example, stimuli presented to the participant or participant responses.

    Examples
    --------
    >>> event = BIDSTaskEvent(onset=1.0, duration=0)

    Notes
    -----
    For more details on task event files, see [BIDS Specification](https://bids-specification.readthedocs.io/en/stable/04-modality-specific-files/05-task-events.html).
    """

    def __init__(
        self,
        onset: Union[int, float, str],
        duration: Union[int, float, str],
        *args: tuple,
        trial_type: Union[str, None] = None,
        sample: Union[int, str, None] = None,
        response_time: Union[int, float, str, None] = None,
        value: object = None,
        hed: Union[str, None] = None,
        stim_file: Union[str, None] = None,
        identifier: Union[str, None] = None,
        database: Union[str, None] = None,
        **kwargs: dict,
    ) -> None:
        """Initialize a BIDSTaskEvent object.

        Parameters
        ----------
        onset : int, float, str
            Onset (in seconds) of the event, measured from the beginning of the acquisition of the
            first data point stored in the corresponding task data file.
        duration : int, float, str
            Duration of the event (measured from onset) in seconds.
        *args : tuple
            Any arguments that the object's superclass's `__init__` method might require.
        trial_type : str, optional
            Primary categorisation of each trial to identify them as instances of the experimental
            conditions.
        sample : int, str, optional
            Onset of the event according to the sampling scheme of the recorded modality.
        response_time : int, float, str, optional
            Marker value associated with the event.
        value : object, optional
            Marker value associated with the event.
        hed : str, optional
            Hierarchical Event Descriptor (HED) Tag.
        stim_file : str, optional
            Represents the location of the stimulus file (such as an image, video, or audio file)
            presented at the given onset time.
        identifier : str, optional
            Represents the database identifier of the stimulus file presented at the given onset
            time.
        database : str, optional
            Represents the database of the stimulus file presented at the given onset time.
        **kwargs : dict
            Any keyword arguments that the object's superclass's `__init__` method might require.
        """
        super().__init__(*args, **kwargs)
        self.__dict__ = self

        self["onset"] = self._validateOnset(onset)
        self["duration"] = self._validateDuration(duration)
        self["trial_type"] = self._validateAttribute("trial_type", trial_type)
        self["sample"] = self._validateSample(sample)
        self["response_time"] = self._validateResponseTime(response_time)
        self["value"] = value
        self["hed"] = self._validateAttribute("hed", hed)
        self["stim_file"] = self._validateAttribute("stim_file", stim_file)
        self["identifier"] = self._validateAttribute("identifier", identifier)
        self["database"] = self._validateAttribute("database", database)

    # -------------------------------------------------------------------------------------------- #

    def __setitem__(self, key: str, value: object) -> None:
        """Set the value associated with a specific key.

        If the key already exists in the event, the new value will be validated using
        the `_validateAttribute` method before being set.

        Parameters
        ----------
        key : str
            The key for which to set the value.
        value : object
            The value to be associated with the key.
        """

        if key == "onset":
            value = self._validateOnset(value)
        if key == "duration":
            value = self._validateDuration(value)
        if key in ["trial_type, hed, stim_file, identifier, database"]:
            value = self._validateAttribute(key, value)
        if key == "sample":
            value = self._validateSample(value)
        if key == "response_time":
            value = self._validateResponseTime(value)

        super().__setitem__(key, value)

    # -------------------------------------------------------------------------------------------- #

    def __repr__(self) -> str:
        """Return a printable representational string of the given object.

        This method returns a string representation of the BIDSTaskEvent object containing its
        attribute-value pairs.

        Returns:
        -------
        str
            A string representation of the BIDSTaskEvent object.
        """
        msg = f"BIDSTaskEvent({', '.join(f'{k}={v}' for k, v in self.items() if v is not None)})"
        return msg

    # -------------------------------------------------------------------------------------------- #

    @staticmethod
    def _validateOnset(value: Union[int, float, str]) -> float:
        """Validate and format the onset value.

        This method ensures that the onset value is a numeric type or can be successfully converted
        to a float. If the value is provided as a string, it must be a numeric string (containing
        only digits).

        Parameters
        ----------
        value : int, float, str
            The onset value to be validated. Can be provided as an int, float, or numeric string.

        Returns
        -------
        float
            The validated onset value, rounded to four decimal places.

        Raises
        ------
        OnsetError
            If the provided onset value is not a valid numeric type or string.
        """
        if isinstance(value, (int, float)):
            return round(value, 4)
        if isinstance(value, str) and value.isnumeric():
            return round(float(value), 4)
        raise OnsetError(value)

    # -------------------------------------------------------------------------------------------- #

    @staticmethod
    def _validateDuration(value: Union[int, float, str]) -> Union[float, str]:
        """Validate and process the duration value.

        This method checks the provided value and validates whether it represents a valid
        duration for an event. Valid duration values include non-negative integers or floats,
        as well as the string "n/a". If the provided value is numeric as a string, it is
        converted to a float before validation.

        Parameters
        ----------
        value : int, float, str
            The value to be validated as a valid event duration.

        Returns
        -------
        float or str
            The processed and validated duration value.

        Raises
        ------
        DurationError
            If the provided value is not a valid event duration.
        """
        if value == "n/a":
            return value
        if isinstance(value, (int, float)) and value >= 0:
            return round(value, 4)
        if isinstance(value, str) and value.isnumeric():
            return round(float(value), 4)
        raise DurationError(value)

    # -------------------------------------------------------------------------------------------- #

    @staticmethod
    def _validateSample(value: Union[int, str, None]) -> Union[int, None]:
        """Validate and process the sample value.

        This method checks the provided value and validates whether it represents a valid sample
        index for an event. Valid sample values include positive integers. If the provided value is
        numeric as a string, it is converted to an integer before validation.

        Parameters
        ----------
        value : int or str
            The value to be validated as a valid sample index.

        Returns
        -------
        int or None
            The processed and validated sample index, or None if the value is not valid.

        Raises
        ------
        SampleError
            If the provided value is not a valid sample index.
        """
        if isinstance(value, int):
            return value
        if isinstance(value, str) and value.isnumeric():
            return int(value)
        if value:
            raise SampleError(value)
        return None

    # -------------------------------------------------------------------------------------------- #
    @staticmethod
    def _validateResponseTime(
        value: Union[int, float, str, None]
    ) -> Union[float, str, None]:
        """Validate and process the response time value.

        This method checks the provided value and validates whether it represents a valid response
        time for an event. Valid response time values include non-negative integers, floats, as well
        as the string "n/a". If the provided value is numeric as a string, it is converted to a
        float before validation.

        Parameters
        ----------
        value : int or float or str
            The value to be validated as a valid response time.

        Returns
        -------
        float or str or None
            The processed and validated response time value, or None if the value is not valid.

        Raises
        ------
        ResponseTimeError
            If the provided value is not a valid response time.
        """
        if value == "n/a":
            return value
        if isinstance(value, str) and value.isnumeric():
            return round(float(value), 4)
        if isinstance(value, (int, float)):
            return round(value, 4)
        if value:
            raise ResponseTimeError(value)
        return None

    # -------------------------------------------------------------------------------------------- #
    @staticmethod
    def _validateAttribute(key: str, value: object) -> Union[str, None]:
        """Validate and process an attribute value.

        This method performs validation on an attribute value. If the value is not None,
        it checks whether it's an instance of string. If it's a string, it is returned as-is.
        If the value is not a string, an error class corresponding to the key's name is raised.

        Parameters
        ----------
        key : str
            The key representing the attribute's name.
        value : object
            The value to be validated.

        Returns
        -------
        str or None
            The validated string value or None if the value is None.

        Raises
        ------
        AttributeError
            If the provided value is not a valid string attribute.
        """
        if value is not None:
            if isinstance(value, str):
                return value

            error_class = globals()[
                f"{key.replace('_', ' ').title().replace(' ','')}Error"
            ]
            raise error_class(value)
        return None

    # -------------------------------------------------------------------------------------------- #

    @property
    def onset(self):
        """
        Onset (in seconds) of the event, measured from the beginning of the acquisition of the
        first data point stored in the corresponding task data file.
        """
        return self.get("onset")

    @onset.setter
    def onset(self, onset):
        self["onset"] = self._validateOnset(onset)

    # -------------------------------------------------------------------------------------------- #

    @property
    def duration(self) -> float:
        """
        Duration of the event (measured from onset) in seconds.
        """
        return self.get("duration")

    @duration.setter
    def duration(self, duration: float) -> None:
        self["duration"] = self._validateDuration(duration)

    # -------------------------------------------------------------------------------------------- #

    @property
    def trial_type(self):
        """
        Primary categorisation of each trial to identify them as instances of the experimental
        conditions.
        """
        return self.get("trial_type")

    @trial_type.setter
    def trial_type(self, trial_type):
        self["trial_type"] = self._validateAttribute("trial_type", trial_type)

    # -------------------------------------------------------------------------------------------- #

    @property
    def sample(self):
        """
        Onset of the event according to the sampling scheme of the recorded modality.
        """
        return self.get("sample")

    @sample.setter
    def sample(self, sample):
        self["sample"] = self._validateSample(sample)

    # -------------------------------------------------------------------------------------------- #

    @property
    def response_time(self):
        """
        Response time measured in seconds.
        """
        return self.get("response_time")

    @response_time.setter
    def response_time(self, response_time):
        self["response_time"] = self._validateResponseTime(response_time)

    # -------------------------------------------------------------------------------------------- #

    @property
    def value(self):
        """
        Marker value associated with the event.
        """
        return self.get("value")

    @value.setter
    def value(self, value):
        self["value"] = self._validateAttribute("value", value)

    # -------------------------------------------------------------------------------------------- #

    @property
    def hed(self):
        """
        Hierarchical Event Descriptor (HED) Tag.
        """
        return self.get("hed")

    @hed.setter
    def hed(self, hed):
        self["hed"] = self._validateAttribute("hed", hed)

    # -------------------------------------------------------------------------------------------- #

    @property
    def stim_file(self):
        """
        Represents the location of the stimulus file (such as an image, video, or audio file)
        presented at the given onset time.
        """
        return self.get("stim_file")

    @stim_file.setter
    def stim_file(self, stim_file):
        self["stim_file"] = self._validateAttribute("stim_file", stim_file)

    # -------------------------------------------------------------------------------------------- #

    @property
    def identifier(self):
        """
        Represents the database identifier of the stimulus file presented at the given onset time.
        """
        return self.get("identifier")

    @identifier.setter
    def identifier(self, identifier):
        self["identifier"] = self._validateAttribute("identifier", identifier)

    # -------------------------------------------------------------------------------------------- #

    @property
    def database(self):
        """
        Represents the database of the stimulus file presented at the given onset time.
        """
        return self.get("database")

    @database.setter
    def database(self, database):
        self["database"] = self._validateAttribute("database", database)


# ----------------------------------------------------------------------------------------------- #


class BIDSError(Exception):
    """
    Base class for all BIDS-related exceptions.

    This class serves as the base exception class for all exceptions related to BIDS (Brain
    Imaging Data Structure) specifications and operations.
    """


# ----------------------------------------------------------------------------------------------- #


class OnsetError(BIDSError):
    """Exception raised when onset value is incorrect.

    This exception is raised when the provided onset value does not meet the expected criteria
    for correctness according to BIDS (Brain Imaging Data Structure) specifications.
    """

    def __init__(
        self, onset: object, msg: str = "Property 'onset' MUST be a number"
    ) -> None:
        """Initialize the OnsetError instance.

        Parameters
        ----------
        onset : object
            The onset value that caused the error.
        msg : str, optional
            Explanation of the error.
        """
        self.onset = onset
        self.msg = msg
        super().__init__(self.msg)

    def __str__(self) -> str:
        """Return a string representation of the error.

        Returns
        -------
        str
            A string containing the onset value and the error message.
        """
        return f"{self.onset} -> {self.msg}"


# ----------------------------------------------------------------------------------------------- #


class DurationError(BIDSError):
    """Exception raised when duration value is incorrect.

    This exception is raised when the provided duration value does not meet the expected criteria
    for correctness according to BIDS (Brain Imaging Data Structure) specifications.
    """

    def __init__(
        self,
        duration: object,
        msg: str = "Property 'duration' MUST be either zero or positive (or n/a if unavailable)",
    ) -> None:
        """Initialize the DurationError instance.

        Parameters
        ----------
        duration : object
            The duration value that caused the error.
        msg : str, optional
            Explanation of the error.
        """
        self.duration = duration
        self.msg = msg
        super().__init__(self.msg)

    def __str__(self) -> str:
        """Return a string representation of the error.

        Returns
        -------
        str
            A string containing the duration value and the error message.
        """
        return f"{self.duration} -> {self.msg}"


# ----------------------------------------------------------------------------------------------- #


class TrialTypeError(BIDSError):
    """Exception raised when trial_type value is incorrect.

    This exception is raised when the provided trial_type value does not meet the expected criteria
    for correctness according to BIDS (Brain Imaging Data Structure) specifications.
    """

    def __init__(
        self, trial_type: object, msg: str = "Property 'trial_type' MUST be a string"
    ) -> None:
        """Initialize the TrialTypeError instance.

        Parameters
        ----------
        trial_type : object
            The trial_type value that caused the error.
        msg : str, optional
            Explanation of the error.
        """
        self.trial_type = trial_type
        self.msg = msg
        super().__init__(self.msg)

    def __str__(self) -> str:
        """Return a string representation of the error.

        Returns
        -------
        str
            A string containing the trial_type value and the error message.
        """
        return f"{self.trial_type} -> {self.msg}"


# ----------------------------------------------------------------------------------------------- #


class SampleError(BIDSError):
    """Exception raised when sample value is incorrect.

    This exception is raised when the provided sample value does not meet the expected criteria
    for correctness according to BIDS (Brain Imaging Data Structure) specifications.
    """

    def __init__(
        self, sample: object, msg: str = "Property 'sample' MUST be an integer"
    ) -> None:
        """Initialize the SampleError instance.

        Parameters
        ----------
        sample : object
            The sample value that caused the error.
        msg : str, optional
            Explanation of the error.
        """
        self.sample = sample
        self.msg = msg
        super().__init__(self.msg)

    def __str__(self) -> str:
        """Return a string representation of the error.

        Returns
        -------
        str
            A string containing the sample value and the error message.
        """
        return f"{self.sample} -> {self.msg}"


# ----------------------------------------------------------------------------------------------- #


class ResponseTimeError(BIDSError):
    """Exception raised when response_time value is incorrect.

    This exception is raised when the provided response_time value does not meet the expected
    criteria for correctness according to BIDS (Brain Imaging Data Structure) specifications.
    """

    def __init__(
        self,
        response_time: object,
        msg: str = "Property 'response_time' MUST be a number (or n/a if unavailable)",
    ) -> None:
        """Initialize the ResponseTimeError instance.

        Parameters
        ----------
        response_time : object
            The response_time value that caused the error.
        msg : str, optional
            Explanation of the error.
        """
        self.response_time = response_time
        self.msg = msg
        super().__init__(self.msg)

    def __str__(self) -> str:
        """Return a string representation of the error.

        Returns
        -------
        str
            A string containing the response_time value and the error message.
        """
        return f"{self.response_time} -> {self.msg}"


# ----------------------------------------------------------------------------------------------- #


class HedError(BIDSError):
    """Exception raised when hed value is incorrect.

    This exception is raised when the provided hed value does not meet the expected criteria
    for correctness according to BIDS (Brain Imaging Data Structure) specifications.
    """

    def __init__(
        self, hed: object, msg: str = "Property 'hed' MUST be a string"
    ) -> None:
        """Initialize the HEDError instance.

        Parameters
        ----------
        hed : object
            The hed value that caused the error.
        msg : str, optional
            Explanation of the error.
        """
        self.hed = hed
        self.msg = msg
        super().__init__(self.msg)

    def __str__(self) -> str:
        """Return a string representation of the error.

        Returns
        -------
        str
            A string containing the hed value and the error message.
        """
        return f"{self.hed} -> {self.msg}"


# ----------------------------------------------------------------------------------------------- #


class StimFileError(BIDSError):
    """Exception raised when stim_file value is incorrect.

    This exception is raised when the provided stim_file value does not meet the expected criteria
    for correctness according to BIDS (Brain Imaging Data Structure) specifications.
    """

    def __init__(
        self, stim_file: object, msg: str = "Property 'stim_file' MUST be a string"
    ) -> None:
        """Initialize the StimFileError instance.

        Parameters
        ----------
        stim_file : object
            The stim_file value that caused the error.
        msg : str, optional
            Explanation of the error.
        """
        self.stim_file = stim_file
        self.msg = msg
        super().__init__(self.msg)

    def __str__(self) -> str:
        """Return a string representation of the error.

        Returns
        -------
        str
            A string containing the stim_file value and the error message.
        """
        return f"{self.stim_file} -> {self.msg}"


# ----------------------------------------------------------------------------------------------- #


class IdentifierError(BIDSError):
    """Exception raised when identifier value is incorrect.

    This exception is raised when the provided identifier value does not meet the expected criteria
    for correctness according to BIDS (Brain Imaging Data Structure) specifications.
    """

    def __init__(
        self, identifier: object, msg: str = "Property 'identifier' MUST be a string"
    ) -> None:
        """Initialize the IdentifierError instance.

        Parameters
        ----------
        identifier : object
            The identifier value that caused the error.
        msg : str, optional
            Explanation of the error.
        """
        self.identifier = identifier
        self.msg = msg
        super().__init__(self.msg)

    def __str__(self) -> str:
        """Return a string representation of the error.

        Returns
        -------
        str
            A string containing the identifier value and the error message.
        """
        return f"{self.identifier} -> {self.msg}"


# ----------------------------------------------------------------------------------------------- #


class DatabaseError(BIDSError):
    """Exception raised when database value is incorrect.

    This exception is raised when the provided database value does not meet the expected criteria
    for correctness according to BIDS (Brain Imaging Data Structure) specifications.
    """

    def __init__(
        self, database: object, msg: str = "Property 'database' MUST be a string"
    ) -> None:
        """Initialize the DatabaseError instance.

        Parameters
        ----------
        database : object
            The database value that caused the error.
        msg : str, optional
            Explanation of the error.
        """
        self.database = database
        self.msg = msg
        super().__init__(self.msg)

    def __str__(self) -> str:
        """Return a string representation of the error.

        Returns
        -------
        str
            A string containing the database value and the error message.
        """
        return f"{self.database} -> {self.msg}"
