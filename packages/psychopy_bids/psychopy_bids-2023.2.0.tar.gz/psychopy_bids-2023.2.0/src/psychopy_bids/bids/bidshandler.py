"""This module provides the class BIDSHandler"""

import json
import os
import platform
import re
import shutil
import sys
import warnings
from ast import literal_eval
from datetime import datetime
from pathlib import Path
from typing import Union

import numpy as np
import pandas as pd
import requests

from psychopy_bids.bids.bidsbehevent import BIDSBehEvent
from psychopy_bids.bids.bidstaskevent import BIDSTaskEvent


class BIDSHandler:
    """A class to handle the creation of a BIDS-compliant dataset.

    This class provides methods for creating and managing BIDS datasets and their modality agnostic
    files plus modality specific files.

    Examples
    --------
    >>> handler = BIDSHandler(dataset="/path/to/your/dataset")
    """

    def __init__(
        self,
        dataset: str,
        subject: Union[str, None] = None,
        task: Union[str, None] = None,
        session: Union[str, None] = None,
        data_type: str = "beh",
        acq: Union[str, None] = None,
        runs: bool = True,
    ) -> None:
        """Initialize a BIDSHandler object.

        Parameters
        ----------
        dataset : str
            A set of neuroimaging and behavioral data acquired for a purpose of a particular study.
        subject : str, optional
            A person or animal participating in the study.
        task : str, optional
            A set of structured activities performed by the participant.
        session : str, optional
            A logical grouping of neuroimaging and behavioral data consistent across subjects.
        data_type : str, optional
            A functional group of different types of data.
        acq : str, optional
            Custom label to distinguish different conditions present during multiple runs of the
            same task.
        runs : bool, optional
            If True, run will be added to filename.
        """
        self.dataset = dataset
        self.subject = subject
        self.task = task
        self.session = session
        self.data_type = data_type
        self.acq = acq
        self.runs = runs

    # -------------------------------------------------------------------------------------------- #

    def _addEvents(self, events: list, participant_info: dict, event_type: str) -> Path:
        """Add events and information of a participant to the dataset.

        This method scans all passed events and information to create the required tabular files.

        Parameters
        ----------
        events : list
            A set of structured activities performed by the participant.
        participant_info : dict
            A dictionary describing properties of each participant (such as age, sex, etc.).
        event_type : str
            The type of events to save. Must be one of "BEH" or "EVENTS".

        Returns
        -------
        file_name : str
            File name of the created tsv event file.
        """
        participants_file = Path(self.dataset) / "participants.tsv"
        participant_info["participant_id"] = self.subject

        # Create the header of the tsv file and add the first subject
        if participants_file.stat().st_size == 0:
            data_frame = pd.DataFrame()
            # Create dict for participants information
            participants = {}
            data_frame = pd.concat([data_frame, pd.DataFrame([participant_info])])
            for info in participant_info:
                participants.update(
                    {
                        info: {
                            "Description": "RECOMMENDED. Free-form natural language description."
                        }
                    }
                )
            with open(
                f"{self.dataset}{os.sep}participants.json", mode="w", encoding="utf-8"
            ) as json_file:
                json.dump(participants, json_file)
            data_frame.to_csv(participants_file, sep="\t", index=False)

        # Update the participants.tsv file
        else:
            data_frame = pd.read_csv(participants_file, sep="\t")
            if self.subject not in data_frame["participant_id"].tolist():
                data_frame = pd.concat(
                    [data_frame, pd.DataFrame(participant_info, index=[0])],
                    ignore_index=True,
                )
                data_frame = data_frame.fillna("n/a")
                data_frame.to_csv(participants_file, sep="\t", index=False)

        # Write the events from the list to the .tsv-file
        if event_type == "events":
            bids_events = [
                entry for entry in events if isinstance(entry, BIDSTaskEvent)
            ]
        else:
            bids_events = [entry for entry in events if isinstance(entry, BIDSBehEvent)]

        # Set the path of the folder and the file
        path_components = [self.dataset, self.subject]
        if self.session:
            path_components.append(self.session)
        path_components.append(self.data_type)
        pth = Path(*path_components)
        pth.mkdir(parents=True, exist_ok=True)

        file_components = [self.subject, self.task]
        if self.session:
            file_components.insert(1, self.session)
        if self.acq:
            file_components.append(self.acq)

        file_components = "_".join(file_components)
        run = list(pth.glob(f"{file_components}*_{event_type}.tsv"))
        if self.runs:
            file_name = f"{file_components}_run-{len(run) + 1}_{event_type}.tsv"
        else:
            file_name = f"{file_components}_{event_type}.tsv"

        # Drop the empty columns and change None values to 'n/a'
        data_frame = pd.DataFrame(bids_events)
        data_frame.fillna(value=np.nan)
        data_frame.dropna(how="all", axis=1, inplace=True)
        data_frame = data_frame.fillna("n/a")

        # Arrange the columns so that onset and duration are at the first two columns
        if "onset" in data_frame.columns and "duration" in data_frame.columns:
            data_frame = data_frame[
                (
                    ["onset", "duration"]
                    + [col for col in data_frame if col not in ["onset", "duration"]]
                )
            ]

        data_frame.to_csv(pth / file_name, sep="\t", index=False)
        return pth / file_name

    # -------------------------------------------------------------------------------------------- #

    def addBehEvents(self, events: list, participant_info: dict) -> str:
        """Add events of type BIDSBehEvent and participant information to the dataset.

        This method uses both the provided BIDSBehEvent events and participant information to
        create the necessary `*_beh.tsv` file, while also making updates to the `participant.tsv`
        file.

        Parameters
        ----------
        events : list
            A set of structured activities performed by the participant.
        participant_info : dict
            A dictionary describing properties of each participant (such as age, sex, etc.).

        Returns
        -------
        file_name : str
            File name of the created tsv event file.

        Examples
        --------
        >>> handler = bids.BIDSHandler(
        ...     dataset="/path/to/your/dataset",
        ...     subject="sub-01",
        ...     task="simple"
        ... )
        >>> handler.addBehEvents(
        ...     events=[bids.BIDSBehEvent(trial=1), bids.BIDSBehEvent(trial=2)],
        ...     participant_info={'participant_id': handler.subject}
        ... )

        Notes
        -----
        For more details on behavioral experiment files, see [BIDS Specification](https://bids-specification.readthedocs.io/en/stable/04-modality-specific-files/07-behavioral-experiments.html).
        """
        return self._addEvents(events, participant_info, "beh")

    # -------------------------------------------------------------------------------------------- #

    def addChanges(
        self, changes: list, version: str = "PATCH", force: bool = False
    ) -> None:
        """Update the version history of the dataset.

        This method updates the CPAN changelog-like file `CHANGES` by adding a new version entry
        with the specified changes and incrementing the version number accordingly.

        Parameters
        ----------
        changes : list
            List of changes or bullet points for the new version.
        version : str, optional
            The version part to increment. Must be one of "MAJOR", "MINOR", or "PATCH".
        force : bool, optional
            Specifies whether existing file should be overwritten.

        Returns
        -------
        None

        Examples
        --------
        >>> handler = bids.BIDSHandler(
        ...     dataset="/path/to/your/dataset/",
        ...     subject=None,
        ...     task=None
        ... )
        >>> handler.addChanges(["Added new data files"], "MAJOR")

        Notes
        -----
        Version history of the dataset (describing changes, updates and corrections) MAY be provided
        in the form of a CHANGES text file. This file MUST follow the CPAN Changelog convention. The
        CHANGES file MUST be either in ASCII or UTF-8 encoding. For more details on the CHANGES
        file, see [BIDS Specification](https://bids-specification.readthedocs.io/en/stable/03-modality-agnostic-files.html#changes).
        """
        changelog_dest = Path(self.dataset) / "CHANGES"
        # Check if the file already exists and if it should be overwritten
        if not force and changelog_dest.exists():
            print(
                "File 'CHANGES' already exists, use force for overwriting it!",
                file=sys.stderr,
            )

        # If the file exists, extract the current version and update it
        if changelog_dest.exists():
            with open(changelog_dest, "r", encoding="utf-8") as file:
                content = file.read()
            matches = re.findall(r"(\d+\.\d+\.\d+)\s+-", content, re.MULTILINE)

            if matches:
                # Determine the latest version and increment it based on the specified version
                curr_version = [
                    int(num) for num in sorted(matches, reverse=True)[0].split(".")
                ]
                new_version = curr_version
                if version == "MAJOR":
                    new_version[0] += 1
                elif version == "MINOR":
                    new_version[1] += 1
                else:
                    new_version[2] += 1
                new_version = ".".join(str(num) for num in new_version)

            # Read the content of the file and prepare the new entry
            with open(changelog_dest, "r", encoding="utf-8") as file:
                content = file.read()
            entry = f"{new_version} - {datetime.now().strftime('%Y-%m-%d')}\n"
            entry += "\n".join([f" - {change}" for change in changes])
            entry += "\n\n" + content
        else:
            # If the file does not exist, create a new entry with version 1.0.0
            entry = f"1.0.0 - {datetime.now().strftime('%Y-%m-%d')}\n"
            entry += "\n".join([f" - {change}" for change in changes])

        with open(changelog_dest, mode="w", encoding="utf-8") as file:
            file.write(entry + "\n\n")

    # -------------------------------------------------------------------------------------------- #

    def addDatasetDescription(self, force: bool = False) -> None:
        """Add a description to the dataset.

        This method adds the required `dataset_description.json` file to the dataset.

        Parameters
        ----------
        force : bool, optional
            Specifies whether existing files should be overwritten.

        Returns
        -------
        None

        Examples
        --------
        >>> handler = bids.BIDSHandler(dataset="/path/to/your/dataset")
        >>> handler.addDatasetDescription()

        Notes:
        -----
        The file `dataset_description.json` is a JSON file describing the dataset. Every dataset
        MUST include this file. For more details, see [BIDS Specification](https://bids-specification.readthedocs.io/en/stable/03-modality-agnostic-files.html#dataset-description).
        """
        dataset_desc = Path(self.dataset) / "dataset_description.json"

        # Check if the file already exists and if it should be overwritten
        if not force and dataset_desc.exists():
            print(
                "File 'dataset_description.json' already exists, use force for overwriting it!",
                file=sys.stderr,
            )
        else:
            # Construct the path to the default file and read its content
            bidsdir = Path(sys.modules["psychopy_bids.bids"].__path__[0])
            ds_desc = bidsdir / "template" / "dataset_description.json"
            with open(ds_desc, mode="r", encoding="utf-8") as read_file:
                ds_info = json.load(read_file)

            # Write the updated file
            ds_info["Name"] = self.dataset
            with open(dataset_desc, "w", encoding="utf-8") as write_file:
                json.dump(ds_info, write_file)

    # -------------------------------------------------------------------------------------------- #

    @staticmethod
    def addJSONSidecar(
        event_file: str,
        existing_file: Union[str, None] = None,
        version: Union[str, None] = None,
    ) -> str:
        """Add a JSON sidecar file.

        This method adds an accompanying JSON sidecar file to support tabular data file
        documentation.

        Parameters
        ----------
        event_file : str
            The path of the accompanying task event file.
        existing_file : str, optional
            The path to an existing sidecar JSON file.
        version : str, optional
            The software version used in the experiment.

        Return
        ------
        file_name : str
            The path of the created json event file.

        Examples
        --------
        >>> handler = bids.BIDSHandler(dataset="/path/to/your/dataset")
        >>> handler.addJSONSidecar("sub-01_ses-1_task-simple_run-1_events.tsv")

        Notes:
        -----
        All tabular data files MAY be accompanied by a JSON file describing the columns in detail.
        For more details on tabular files, see [BIDS Specification](https://bids-specification.readthedocs.io/en/stable/02-common-principles.html#tabular-files).
        """
        try:
            # Try to open and load an existing JSON sidecar file
            with open(existing_file, mode="r", encoding="utf-8") as json_reader:
                sidecar = json.load(json_reader)
        except (FileNotFoundError, TypeError, ValueError) as err:
            if err == ValueError:
                warnings.warn(
                    f"file {existing_file} MUST be a valid JSON file, using default sidecar!"
                )
            else:
                warnings.warn(f"file {existing_file} NOT FOUND, using default sidecar!")
            sidecar = {}
            data_frame = pd.read_csv(event_file, sep="\t")
            # Create default column metadata for the sidecar based on DataFrame columns
            column_names = data_frame.columns.values
            for name in column_names:
                sidecar[name] = {
                    "LongName": "OPTIONAL. Long (unabbreviated) name of the column.",
                    "Description": (
                        "RECOMMENDED. Free-form natural language description. The description of "
                        "the column."
                    ),
                    "Levels": (
                        "RECOMMENDED. For categorical variables: An object of possible values "
                        "(keys) and their descriptions (values)."
                    ),
                    "Units": (
                        "RECOMMENDED. Measurement units for the associated file. SI units in CMIXF"
                        "formatting are RECOMMENDED."
                    ),
                    "TermURL": (
                        "RECOMMENDED. URL pointing to a formal definition of this type of data in"
                        "an ontology available on the web."
                    ),
                    "HED": "OPTIONAL. Hierarchical Event Descriptor (HED) information.",
                }
        finally:
            # Update the sidecar with StimulusPresentation metadata
            sidecar["StimulusPresentation"] = {
                "OperationgSystem": f"{platform.system()} {platform.release()}",
                "SoftwareName": "PsychoPy",
                "SoftwareRRID": "SCR_006571",
            }
            if version:
                sidecar["StimulusPresentation"].update({"SoftwareVersion": version})

        # Get the base name of the event file and create it, if it does not exist
        file_name = os.path.splitext(event_file)[0]
        if not os.path.exists(f"{file_name}.json"):
            with open(f"{file_name}.json", mode="w", encoding="utf-8") as json_file:
                json.dump(sidecar, json_file)
        return file_name

    # -------------------------------------------------------------------------------------------- #

    def addLicense(self, identifier: str, force: bool = False) -> None:
        """Add a license file to the dataset.

        This method downloads a license with the given identifier from the SPDX license list and
        copies the content into the file `LICENSE`.

        Parameters
        ----------
        identifier : str
            Identifier of the license.
        force : bool, optional
            Specifies whether existing file should be overwritten.

        Returns
        -------
        None

        Examples
        --------
        >>> handler = bids.BIDSHandler(dataset="/path/to/your/dataset")
        >>> handler.addLicense("CC-BY-NC-4.0")

        Notes:
        -----
        A LICENSE file MAY be provided in addition to the short specification of the used license in
        the dataset_description.json "License" field. The "License" field and LICENSE file MUST
        correspond. The LICENSE file MUST be either in ASCII or UTF-8 encoding. For more details on
        the LICENSE file, see [BIDS Specification](https://bids-specification.readthedocs.io/en/stable/03-modality-agnostic-files.html#license).
        """

        # Update the 'Licence' field in the dataset description with the provided license
        dataset_desc = Path(self.dataset) / "dataset_description.json"
        if not dataset_desc.exists():
            self.addDatasetDescription()
        with dataset_desc.open("r", encoding="utf-8") as file:
            ds_info = json.load(file)
        ds_info["Licence"] = identifier
        with dataset_desc.open("w", encoding="utf-8") as write_file:
            json.dump(ds_info, write_file)

        # Check if the 'LICENCE' file already exists and if it should be overwritten
        license_dest = Path(self.dataset) / "LICENCE"
        if not force and license_dest.exists():
            print(
                "File 'LICENCE' already exists, use force for overwriting it!",
                file=sys.stderr,
            )
        else:
            # Attempt to download the license text from a remote source based on the identifier
            try:
                response = requests.get(
                    f"https://spdx.org/licenses/{identifier}.txt", timeout=10
                )
                if response.status_code == 200:
                    license_text = response.text
                    with open(license_dest, "w", encoding="utf-8") as file:
                        file.write(license_text)
                else:
                    print(
                        f"License '{identifier}' not found or could not be downloaded.",
                        file=sys.stderr,
                    )
            except requests.exceptions.Timeout:
                print(f"Request to download {identifier} timed out.", file=sys.stderr)
            except requests.exceptions.RequestException as exc:
                print(f"Request error: {exc}", file=sys.stderr)

    # -------------------------------------------------------------------------------------------- #

    def addReadme(self, force: bool = False) -> None:
        """Add a text file explaining the dataset in detail.

        This method adds a `README` template file to the dataset, which contains the main sections
        needed to describe the dataset in more detail.

        Parameters
        ----------
        force : bool, optional
            Specifies whether existing file should be overwritten.

        Returns
        -------
        None

        Examples
        --------
        >>> handler = bids.BIDSHandler(dataset="/path/to/your/dataset")
        >>> handler.addReadme()

        Notes:
        -----
        A REQUIRED text file, README, SHOULD describe the dataset in more detail. A BIDS dataset
        MUST NOT contain more than one README file (with or without extension) at its root
        directory. For more details on the README file, see [BIDS Specification](https://bids-specification.readthedocs.io/en/stable/03-modality-agnostic-files.html#readme).
        """
        readme_dest = Path(self.dataset) / "README"

        # Check if the 'README' file already exists and if it should be overwritten
        if not force and readme_dest.exists():
            print(
                "File 'README' already exists, use force for overwriting it!",
                file=sys.stderr,
            )
        # Copy the content of the template 'README' file to the destination 'README' file
        else:
            bidsdir = Path(sys.modules["psychopy_bids.bids"].__path__[0])
            readme_src = bidsdir / "template" / "README"
            shutil.copyfile(readme_src, readme_dest)

    # -------------------------------------------------------------------------------------------- #

    def addStimuliFolder(self, event_file: str, path: str = "stimuli") -> None:
        """Add stimuli in a stimuli directory.

        This method adds all stimuli represented in an given tsv file into the `/stimuli` directory.

        Parameters
        ----------
        event_file : str
            path of the accompanying task event file.
        path : str, optional
            path to the individual experiment stimuli.

        Returns
        -------
        None

        Examples
        --------
        >>> handler = bids.BIDSHandler(dataset="/path/to/your/dataset")
        >>> handler.addStimuliFolder("sub-01_ses-1_task-simple_run-1_events.tsv")

        Notes
        -----
        The stimulus files can be added in a /stimuli directory (under the root directory of the
        dataset; with optional subdirectories) AND using a stim_file column in events.tsv mentioning
        which stimulus file was used for a given event. For example images/cat03.jpg will be
        translated to /stimuli/images/cat03.jpg. For more details on STIMULI file, see
        [BIDS Specification](https://bids-specification.readthedocs.io/en/stable/04-modality-specific-files/05-task-events.html#stimuli).


        """
        data_frame = pd.read_csv(event_file, sep="\t")
        if "stim_file" in data_frame.columns:
            # Extract unique stimuli from the "stim_file" column
            stimuli = list(data_frame["stim_file"].dropna().unique())
            for stim in stimuli:
                src = Path(path) / stim
                if src.is_file():
                    # Create the necessary directories and copy the source file to the destination
                    stim_dir = Path(self.dataset) / "stimuli"
                    dest_file = stim_dir / stim
                    dest_file.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copyfile(src, dest_file)
                else:
                    warnings.warn(f"File {stim} does not exist!")

    # -------------------------------------------------------------------------------------------- #

    def addTaskEvents(self, events: list, participant_info: dict) -> str:
        """Add events of type BIDSTaskEvent and participant information to the dataset.

        This method uses both the provided BIDSTaskEvent events and participant information to
        create the necessary `*_events.tsv` file, while also making updates to the `participant.tsv`
        file.

        Parameters
        ----------
        events : list
            A set of structured activities performed by the participant.
        participant_info : dict
            A dictionary describing properties of each participant (such as age, sex, etc.).

        Returns
        -------
        file_name : str
            File name of the created tsv event file.

        Examples
        --------
        >>> handler = bids.BIDSHandler(
        ...     dataset="/path/to/your/dataset",
        ...     subject="sub-01",
        ...     task="simple"
        ... )
        >>> handler.addTaskEvents(
        ...     events=[
        ...         BIDSTaskEvent(onset=1.0, duration=0),
        ...         BIDSTaskEvent(onset=2.0, duration=0)
        ...     ],
        ...     participant_info={'participant_id': handler.subject}
        ... )

        Notes
        -----
        For more details on task event files, see [BIDS Specification](https://bids-specification.readthedocs.io/en/stable/04-modality-specific-files/05-task-events.html).
        """
        return self._addEvents(events, participant_info, "events")

    # -------------------------------------------------------------------------------------------- #

    def createDataset(
        self,
        readme: bool = True,
        chg: bool = True,
        lic: bool = True,
        force: bool = False,
    ) -> None:
        """Create the rudimentary body of a new dataset.

        Parameters
        ----------
        readme : bool, optional
            Specifies whether a README file should be created.
        chg : bool, optional
            Specifies whether a CHANGES file should be created.
        lic : bool, optional
            Specifies whether a LICENSE file should be created.
        force : bool, optional
            Specifies whether existing files should be overwritten.

        Returns
        -------
        None

        Examples
        --------
        >>> handler = bids.BIDSHandler(dataset="/path/to/your/dataset")
        >>> handler.createDataset()
        """
        dataset_path = Path(self.dataset)
        # Check if the 'force' parameter is specified
        if not force:
            if dataset_path.exists():
                print(
                    f"The folder {self.dataset} already exists! Use the parameter force if you want"
                    " to recreate a dataset in an existing, non-empty directory",
                    file=sys.stderr,
                )
                return None

        # Create the dataset folder if it doesn't exist
        if not dataset_path.exists():
            dataset_path.mkdir()

        # Create an empty participants.tsv file
        (dataset_path / "participants.tsv").touch()

        # Add description files to the dataset
        self.addDatasetDescription()
        if readme:
            self.addReadme(force=force)
        if chg:
            self.addChanges(changes=["Initialize the dataset"], force=force)
        if lic:
            self.addLicense(identifier="CC-BY-NC-4.0", force=force)
        return None

    # -------------------------------------------------------------------------------------------- #

    @staticmethod
    def parseLog(file, level="BIDS", regex=None) -> list:
        """Extract events from a log file.

        This method parses a given log file based on the specified log level and, optionally, a
        regex pattern. It then processes and structures these events into a list each adhering to
        the BIDSTaskEvent event format.

        Parameters
        ----------
        file : str
            The file path of the log file.
        level : str
            The level name of the bids task events.
        regex : str
            A regular expression to parse the message string.

        Return
        ------
        events : list
            A list of events like presented stimuli or participant responses.

        Examples
        --------
        >>> handler = bids.BIDSHandler(
        ...     dataset="/path/to/your/dataset",
        ...     subject="sub-01",
        ...     task="simple"
        ... )
        >>> log_events = handler.parseLog("simple.log", "BIDS")
        >>> handler.addTaskEvents(
        ...     events=log_events,
        ...     participant_info={'participant_id': handler.subject}
        ... )
        """
        events = []
        try:
            # Open and read the log file line by line
            with open(file, mode="r", encoding="utf-8") as log_file:
                for line in log_file.readlines():
                    event = re.split(r" \t|[ ]+", line, maxsplit=2)
                    # Check if the specified log level matches the event's level
                    if level in event:
                        # If a regex pattern is provided, attempt to match it in the event's message
                        if regex:
                            match = re.search(regex, event[2])
                            if match:
                                entry = match.groupdict()
                            else:
                                entry = {}

                        # If no regex pattern, parse event's message as a dictionary
                        else:
                            entry = {
                                k: v
                                for k, v in literal_eval(event[2]).items()
                                if v is not None
                            }

                        # Add default 'onset' and 'duration' fields if missing
                        if "onset" not in entry.keys():
                            entry.update({"onset": float(event[0])})
                        if "duration" not in entry.keys():
                            entry.update({"duration": "n/a"})
                        events.append(entry)

        except FileNotFoundError:
            warnings.warn(f"file {file} NOT FOUND!")
        return events

    # -------------------------------------------------------------------------------------------- #

    @property
    def dataset(self):
        """
        A set of neuroimaging and behavioral data acquired for a purpose of a particular study.
        """
        return self.__dataset

    @dataset.setter
    def dataset(self, dataset):
        self.__dataset = str(dataset)

    # -------------------------------------------------------------------------------------------- #
    @property
    def subject(self):
        """
        A participant identifier of the form sub-<label>, matching a participant entity found in
        the dataset.
        """
        return self.__subject

    @subject.setter
    def subject(self, subject):
        match = re.match("^sub-[0-9a-zA-Z]+$", str(subject))
        if match:
            self.__subject = subject
        else:
            subject = re.sub("[^A-Za-z0-9]+", "", str(subject))
            self.__subject = f"sub-{subject}"

    # -------------------------------------------------------------------------------------------- #

    @property
    def task(self):
        """
        A set of structured activities performed by the participant.
        """
        return self.__task

    @task.setter
    def task(self, task):
        regex = re.compile("^task-[0-9a-zA-Z]+$", re.I)
        match = regex.match(str(task))
        if match:
            self.__task = task
        else:
            task = re.sub("[^A-Za-z0-9]+", "", str(task))
            self.__task = f"task-{task}"

    # -------------------------------------------------------------------------------------------- #

    @property
    def session(self):
        """
        A logical grouping of neuroimaging and behavioral data consistent across subjects.
        """
        return self.__session

    @session.setter
    def session(self, session):
        if session:
            regex = re.compile("^ses-[0-9a-zA-Z]+$", re.I)
            match = regex.match(str(session))
            if match:
                self.__session = session
            else:
                session = re.sub("[^A-Za-z0-9]+", "", str(session))
                self.__session = f"ses-{session}"
        else:
            self.__session = None

    # -------------------------------------------------------------------------------------------- #

    @property
    def data_type(self):
        """
        A functional group of different types of data.
        """
        return self.__data_type

    @data_type.setter
    def data_type(self, data_type):
        types = [
            "anat",
            "beh",
            "dwi",
            "eeg",
            "fmap",
            "func",
            "ieeg",
            "meg",
            "micr",
            "perf",
            "pet",
        ]
        msg = f"<data_type> MUST be one of the following: {types}"
        if str(data_type) in types:
            self.__data_type = str(data_type)
        else:
            sys.exit(msg)

    # -------------------------------------------------------------------------------------------- #

    @property
    def acq(self):
        """
        A label to distinguish a different set of parameters used for acquiring the same modality.
        """
        return self.__acq

    @acq.setter
    def acq(self, acq):
        if acq:
            regex = re.compile("^acq-[0-9a-zA-Z]+$", re.I)
            match = regex.match(str(acq))
            if match:
                self.__acq = acq
            else:
                acq = re.sub("[^A-Za-z0-9]+", "", str(acq))
                self.__acq = f"acq-{acq}"
        else:
            self.__acq = None
