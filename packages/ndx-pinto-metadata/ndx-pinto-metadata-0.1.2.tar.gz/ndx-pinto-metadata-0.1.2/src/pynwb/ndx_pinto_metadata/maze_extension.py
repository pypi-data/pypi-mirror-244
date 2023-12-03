import os
from pynwb import load_namespaces, register_class
from pynwb.file import DynamicTable
from hdmf.utils import docval, get_docval

spec_path = os.path.abspath(os.path.dirname(__file__))
ns_path = os.path.join(spec_path, "spec", "ndx-pinto-metadata.namespace.yaml")

load_namespaces(ns_path)


@register_class("MazeExtension", "ndx-pinto-metadata")
class MazeExtension(DynamicTable):
    """
    Table for storing maze information
    """

    mazes_attributes = [
        "NoiseDensity",
        "antiFraction",
        "blockPerform",
        "coherenceDist",
        "criteriaNTrials",
        "cueDensityPerM",
        "cueDrawLength",
        "cueDuration",
        "cueProbability",
        "cueVisibleAt",
        "delayLength",
        "easyBlock",
        "easyBlockNTrials",
        "geoDistP",
        "geoDistPEasy",
        "hideCue",
        "hideHintUntil",
        "hideSample",
        "hideTest",
        "lContext",
        "lCue",
        "lMemory",
        "lStart",
        "maxBias",
        "maxTrialDuration",
        "nextMaze",
        "numBlockTrials",
        "numSessions",
        "numTrials",
        "numTrialsPerMin",
        "performance",
        "sampleCoherence",
        "sampleCoherenceSigma",
        "sampleCoherenceTau",
        "sampleDrawLength",
        "sampleLength",
        "startLength",
        "startPosition",
        "testCoherence",
        "testLength",
        "towers",
        "turnHint",
        "varDelayGain",
        "varSampleGain",
        "world",
    ]

    __columns__ = tuple(
        {
            "name": attr,
            "description": "maze information",
            "required": False,
        }
        for attr in mazes_attributes
    )

    @docval(
        dict(name="name", type=str, doc="name of this MazeExtension"),  # required
        dict(name="description", type=str, doc="Description of this DynamicTable"),
        *get_docval(DynamicTable.__init__, "id", "columns", "colnames")
    )
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
