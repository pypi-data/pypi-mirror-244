#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    PsychoPy routine for settings if BIDS class
"""

# Part of the PsychoPy library
# Copyright (C) 2002-2018 Jonathan Peirce (C) 2019-2021 Open Science Tools Ltd.
# Distributed under the terms of the GNU General Public License (GPL).
#


from pathlib import Path

from psychopy.experiment import Param
from psychopy.experiment.routines._base import BaseStandaloneRoutine
from psychopy.localization import _translate

_localized = {}

_localized.update(
    {
        "path": _translate("Path"),
        "runs": _translate("Add runs to event file name"),
    }
)


class BidsExportRoutine(BaseStandaloneRoutine):
    """An event class for inserting arbitrary code into Builder experiments"""

    categories = ["BIDS"]
    targets = ["PsychoPy"]
    iconFile = Path(__file__).parent / "BIDS.png"
    tooltip = _translate(
        "BIDS export: creates BIDS structure, writes tsv file and update"
        " further files"
    )

    def __init__(
        self,
        exp,
        name="bids",
        experiment_bids="bids",
        data_type="beh",
        acq="",
        event_json="",
        runs=True,
        bids_license="CC-BY-NC-4.0",
    ):
        # Initialise base routine
        BaseStandaloneRoutine.__init__(self, exp, name=name)

        self.exp.requireImport(
            importName="BIDSHandler", importFrom="psychopy_bids.bids"
        )

        self.type = "BIDSexport"

        # params
        # self.params = {}

        # Basic params
        self.order += ["data_type", "experiment_bids", "acq", "event_json"]

        self.params["name"].hint = _translate(
            "Name of the task. No two tasks should have the same name."
        )
        self.params["name"].label = _translate("task name")

        hnt = _translate(
            "Name of the experiment (parent folder), if this (task) is part of"
            " a larger one."
        )
        self.params["experiment_bids"] = Param(
            experiment_bids,
            valType="str",
            inputType="single",
            categ="Basic",
            allowedTypes=[],
            canBePath=False,
            hint=hnt,
            label=_translate("experiment name"),
        )

        hnt = _translate("BIDS defined data type")
        self.params["data_type"] = Param(
            data_type,
            valType="str",
            inputType="choice",
            categ="Basic",
            allowedVals=[
                "func",
                "dwi",
                "fmap",
                "anat",
                "perf",
                "meg",
                "eeg",
                "ieeg",
                "beh",
                "pet",
                "micr",
            ],
            hint=hnt,
            label=_translate("data type"),
        )

        hnt = _translate(
            "Custom label to distinguish different conditions present during"
            " multiple runs of the same task"
        )
        self.params["acq"] = Param(
            acq,
            valType="str",
            inputType="single",
            categ="Basic",
            allowedVals=[],
            canBePath=False,
            hint=hnt,
            label=_translate("acquisition mode"),
        )

        hnt = _translate(
            "Name of the default event JSON file. Will be copied into each"
            " subject folder."
        )
        self.params["event_json"] = Param(
            event_json,
            valType="str",
            inputType="single",
            categ="Basic",
            allowedVals=[],
            hint=hnt,
            label=_translate("event JSON"),
        )

        # license
        hnt = _translate("License of the dataset")
        self.params["bids_license"] = Param(
            bids_license,
            valType="str",
            inputType="choice",
            categ="Basic",
            allowedVals=[
                "CC0-1.0",
                "CC-BY-4.0",
                "CC-BY-SA-4.0",
                "CC-BY-ND-4.0",
                "CC-BY-NC-4.0",
                "CC-BY-NC-SA-4.0",
                "CC-BY-NC-ND-4.0",
                "ODC-By-1.0",
                "ODbL-1.0",
                "PDDL-1.0",
                "GFDL-1.3-or-later",
            ],
            hint=hnt,
            label=_translate("license"),
        )

        # runs params
        hnt = _translate("Should runs be added to event file name?")
        self.params["runs"] = Param(
            runs,
            valType="bool",
            inputType="bool",
            categ="Basic",
            hint=hnt,
            label=_translate("Add runs to event filename"),
        )

        # these inherited params are harmless but might as well trim:
        for parameter in (
            "startType",
            "startVal",
            "startEstim",
            "stopVal",
            "stopType",
            "durationEstim",
            "saveStartStop",
            "syncScreenRefresh",
        ):
            if parameter in self.params:
                del self.params[parameter]

    def writeStartCode(self, buff):
        """Code for the start of the experiment"""
        original_indent_level = buff.indentLevel
        inits = self.params

        code = (
            "# create initial folder structure\n"
            "if expInfo['session']:\n"
        )
        buff.writeIndentedLines(code)
        buff.setIndentLevel(1, relative=True)
        code = (
            "bids_handler = BIDSHandler(dataset=%(experiment_bids)s,\n"
            " subject=expInfo['participant'], task=expInfo['expName'],\n"
            " session=expInfo['session'], data_type=%(data_type)s, acq=%(acq)s,\n"
            " runs=%(runs)s)\n"
        )
        buff.writeIndentedLines(code % inits)
        buff.setIndentLevel(-1, relative=True)
        code = "else:"
        buff.writeIndentedLines(code)
        buff.setIndentLevel(1, relative=True)
        code = (
            "bids_handler = BIDSHandler(dataset=%(experiment_bids)s,\n"
            " subject=expInfo['participant'], task=expInfo['expName'],\n"
            " data_type=%(data_type)s, acq=%(acq)s, runs=%(runs)s)\n"
        )
        buff.writeIndentedLines(code % inits)
        buff.setIndentLevel(-1, relative=True)
        code = (
            "bids_handler.createDataset()\n"
            "bids_handler.addLicense(%(bids_license)s)\n"
        )
        buff.writeIndentedLines(code % inits)
        buff.setIndentLevel(original_indent_level)

    def writeExperimentEndCode(self, buff):
        """write code at the end of the experiment"""
        original_indent_level = buff.indentLevel
        inits = self.params

        code = (
            "# get participant_info and events from the ExperimentHandler\n"
            "ignore_list = [\n"
        )
        buff.writeIndentedLines(code % inits)
        buff.setIndentLevel(1, relative=True)
        code = (
            "'participant',\n"
            "'session',\n"
            "'date',\n"
            "'expName',\n"
            "'psychopyVersion',\n"
            "'OS',\n"
            "'frameRate'\n"
        )
        buff.writeIndentedLines(code % inits)
        buff.setIndentLevel(-1, relative=True)
        code = (
            "]\n"
            "participant_info = {\n"
        )
        buff.writeIndentedLines(code % inits)
        buff.setIndentLevel(1, relative=True)
        code = (
            "key: thisExp.extraInfo[key]\n"
            "for key in thisExp.extraInfo\n"
            "if key not in ignore_list\n"
        )
        buff.writeIndentedLines(code % inits)
        buff.setIndentLevel(-1, relative=True)
        code = (
            "}\n"
            "# write tsv file and update\n"
            "try:\n"
        )
        buff.writeIndentedLines(code % inits)
        buff.setIndentLevel(1, relative=True)
        code = "events = [\n"
        buff.writeIndentedLines(code % inits)
        buff.setIndentLevel(1, relative=True)
        code = (
            "value\n"
            "for dictionary in thisExp.getAllEntries()\n"
            "for value in dictionary.values()\n"
            "if isinstance(value, BIDSBehEvent)\n"
        )
        buff.writeIndentedLines(code % inits)
        buff.setIndentLevel(-1, relative=True)
        code = (
            "]\n"
            "if any(isinstance(item, BIDSBehEvent) for item in events):\n"
        )
        buff.writeIndentedLines(code % inits)
        buff.setIndentLevel(1, relative=True)
        code = "event_file = bids_handler.addBehEvents(events, participant_info)\n"
        buff.writeIndentedLines(code % inits)
        buff.setIndentLevel(-1, relative=True)
        code = "else:\n"
        buff.writeIndentedLines(code % inits)
        buff.setIndentLevel(1, relative=True)
        code = "event_file = bids_handler.addTaskEvents(events, participant_info)\n"
        buff.writeIndentedLines(code % inits)
        buff.setIndentLevel(-1, relative=True)
        code = "bids_handler.addJSONSidecar(\n"
        buff.writeIndentedLines(code % inits)
        buff.setIndentLevel(1, relative=True)
        code = (
            "event_file,\n"
            "%(event_json)s,\n"
            "thisExp.extraInfo['psychopyVersion']\n"
        )
        buff.writeIndentedLines(code % inits)
        buff.setIndentLevel(-1, relative=True)
        code = (
            ")\n"
            "bids_handler.addStimuliFolder(event_file)\n"
        )
        buff.writeIndentedLines(code % inits)
        buff.setIndentLevel(-1, relative=True)
        code = "except KeyError:\n"
        buff.writeIndentedLines(code % inits)
        buff.setIndentLevel(1, relative=True)
        code = "pass\n"
        buff.writeIndentedLines(code % inits)
        buff.setIndentLevel(original_indent_level)
