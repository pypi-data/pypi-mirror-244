#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    PsychoPy Builder component for behavioral events
"""

# Part of the PsychoPy library
# Copyright (C) 2002-2018 Jonathan Peirce (C) 2019-2021 Open Science Tools Ltd.
# Distributed under the terms of the GNU General Public License (GPL).

# from os import path
from pathlib import Path

from psychopy.experiment.components import BaseComponent, Param, _translate

# from psychopy import prefs

# only use _localized values for label values, nothing functional:
_localized = {"name": _translate("Name")}

_localized.update(
    {
        "custom": _translate("Custom columns"),
        "add_log": _translate("Add to log file"),
    }
)


class BidsBehEventComponent(BaseComponent):
    """An class for inserting behavioral events into Builder experiments"""

    categories = ["BIDS"]
    targets = ["PsychoPy"]  # , 'PsychoJS'
    iconFile = Path(__file__).parent / "BIDS.png"
    tooltip = _translate("BIDS event: logging of BIDS behavioral events")

    def __init__(
        self,
        exp,
        parentName,
        name="bidsBehEvent",
        custom=None,
        add_log=False,
    ):
        self.type = "BIDSBehEvent"
        self.exp = exp  # so we can access the experiment if necessary
        self.parentName = parentName  # to access the routine too if needed
        self.params = {}
        self.depends = []
        super().__init__(exp, parentName, name=name)

        self.exp.requireImport(
            importName="BIDSBehEvent", importFrom="psychopy_bids.bids"
        )

        self.exp.requireImport(importName="BIDSError", importFrom="psychopy_bids.bids")

        _allow3 = ["constant"]  # , 'set every repeat']  # list

        # Basic params
        self.order += ["custom"]

        hnt = _translate("Add columns as a dictionary")
        self.params["custom"] = Param(
            custom,
            valType="extendedCode",
            inputType="multi",
            allowedTypes=[],
            categ="Basic",
            updates="constant",
            allowedUpdates=_allow3[:],
            canBePath=False,
            hint=hnt,
            label=_localized["custom"],
        )

        # Data params
        hnt = _translate("Should the event be saved in the log file too?")
        self.params["add_log"] = Param(
            add_log,
            valType="bool",
            inputType="bool",
            categ="Data",
            hint=hnt,
            label=_translate("Add event to log"),
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
        """write code in the start of the experimental code"""

        code = "bidsLogLevel = 24\nlogging.addLevel('BIDS', 24)\n"
        if self.params["add_log"]:
            buff.writeIndentedLines(code)

    def writeRoutineEndCode(self, buff):
        """
        write code
        """
        original_indent_level = buff.indentLevel
        inits = self.params

        # what loop are we in (or thisExp)?
        if len(self.exp.flow._loopList):
            curr_loop = self.exp.flow._loopList[-1]  # last (outer-most) loop
        else:
            curr_loop = self.exp._expHandler

        if "Stair" in curr_loop.type:
            add_data_func = "addOtherData"
        else:
            add_data_func = "addData"

        loop = curr_loop.params["name"]
        name = self.params["name"]
        code = "try:\n"
        buff.writeIndentedLines(code % inits)
        buff.setIndentLevel(1, relative=True)
        code = "event = BIDSBehEvent()\n"
        buff.writeIndentedLines(code % inits)
        custom = self.params["custom"]
        if custom:
            code = "event.update(%(custom)s)\n"
            buff.writeIndentedLines(code % inits)
        code = f"{loop}.{add_data_func}('{name}.event', event)\n"
        buff.writeIndentedLines(code % inits)
        buff.setIndentLevel(-1, relative=True)
        code = "except BIDSError:\n"
        buff.writeIndentedLines(code % inits)
        buff.setIndentLevel(1, relative=True)
        code = "pass\n"
        buff.writeIndentedLines(code % inits)
        buff.setIndentLevel(-1, relative=True)

        if self.params["add_log"]:
            code = "logging.log(level=24, msg=dict(event))\n"
            buff.writeIndentedLines(code % inits)

        buff.setIndentLevel(original_indent_level)
