# ndx-pinto-metadata

The NWB extension for storing ViRMEN experimental metadata for the Pinto lab.

## Installation

```bash
pip install ndx_pinto_metadata
```

## Usage

```python
from uuid import uuid4
from datetime import datetime
from dateutil.tz import tzlocal
import numpy as np

from pynwb import NWBFile, NWBHDF5IO
from hdmf.common.table import DynamicTable

from ndx_pinto_metadata import LabMetaDataExtension, MazeExtension

# Create NWBFile
nwbfile = NWBFile(
        session_description="session_description",
        identifier=str(uuid4()),
        session_start_time=datetime(1970, 1, 1, tzinfo=tzlocal()),
    )


# Add MazeExtension
maze_extension = MazeExtension(name="mazes", description="Holds information about the mazes for this task.")
# Add row for each maze
maze_extension.add_row(
    antiFraction=0,
    cueDensityPerM=3,
    cueDuration=np.nan,
    cueProbability=np.inf,
    cueVisibleAt=10,
    hideHintUntil=-15,
    lContext=10,
    lCue=45,
    lMemory=10,
    lStart=5,
    maxTrialDuration=180,
    turnHint=1,
    numTrials=80,
    numTrialsPerMin=2,
    criteriaNTrials=100,
    numSessions=1,
    performance=np.inf,
    maxBias=0.2,
    easyBlock=np.nan,
    easyBlockNTrials=10,
    numBlockTrials=40,
    blockPerform=0.55,
    geoDistP=np.nan,
    geoDistPEasy=np.nan,
)

# Create table for storing stimulus protocol parameters
stimulus_protocol = DynamicTable(name="stimulus_protocol", description="Holds information about the stimulus protocol.")

protocol_dict = dict(
    stimulus_code="TowersTaskSwitchStimulusTrain",
    numMazesInProtocol=11,
    trialDraw="EradeCapped",
    stimDraw="LeftOneOnly",
    cueMinSeparation=12,
    totalRepeatProbability=0.05,
    numRepeatTrials=2,
    visualcolor=np.array([0, 0, 1]),
    memorycolor=np.array([0.5, 0.5, 0.]),
    princetonImplementation=1, 
)
for protocol_name in protocol_dict:
    stimulus_protocol.add_column(
        name=protocol_name,
         description="stimulus protocol parameter.",
    )
stimulus_protocol.add_row(**protocol_dict)

# Create LabMetaData
lab_meta_data = LabMetaDataExtension(
    name="LabMetaData",
    experiment_name="TowersTaskSwitchEasy",
    experiment_code="TowersTaskSwitchEasy",
    session_index=49,
    total_reward=0.925,
    surface_quality=74.22,
    rig="VR_Widefield",
    num_trials=242,
    num_iterations=430233,
    session_duration=3838.5730088,
    advance=0,
    mazes=maze_extension,
    stimulus_protocol=stimulus_protocol,
)

# Add to NWBFile
nwbfile.add_lab_meta_data(lab_meta_data=lab_meta_data)

# Write LabMetaData to NWB file
nwbfile_path = "virmen_metadata.nwb"
with NWBHDF5IO(nwbfile_path, mode="w") as io:
    io.write(nwbfile)
            
# Check LabMetaData was added to the NWB file
with NWBHDF5IO(nwbfile_path, mode="r", load_namespaces=True) as io:
    read_nwbfile = io.read()
    read_nwbfile_lab_metadata = read_nwbfile.lab_meta_data["LabMetaData"]

```

---
This extension was created using [ndx-template](https://github.com/nwb-extensions/ndx-template).
