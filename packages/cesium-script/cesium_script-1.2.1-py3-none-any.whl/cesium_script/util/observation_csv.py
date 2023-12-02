"""
    The CSV input should have a format similar to the CSV export from the SHT
    timeline tool. With the following fields:

OBS_NAME, startTime, endTime, obsRate, SPICE_FOV_name
e.g.:
MAJIS_SAT_DISK_SLEW_001,2032-07-02T10:47:47.000Z,2032-07-02T11:30:30.000Z,,MAJIS

The groups blocks define the start and stop times (startTime, endTime) and the
observation rate (obsRate) for each observation in the series. The observation
rate determines the rate, in seconds, at which footprints will be drawn between
the start and stop times.
Setting the observation rate to 0 will create a continuous swath rather than a
series of footprints. If the obsRate field is left empty it defaults to 0.
"""

import csv
import logging
from dataclasses import dataclass


@dataclass
class Observation:
    name: str
    start: str
    end: str
    rate: str
    fov: str

    def is_valid(self):
        if self.start > self.end:
            logging.warning("End time before start time")
            return False
        return True

    def has_rate(self):
        return len(self.rate.strip()) > 0

    def get_rate(self):
        return int(self.rate) if self.has_rate() else -1


def read_observation_csv(filename):
    with open(filename) as csv_file:
        return read_observation_csvfile(csv_file)


def read_observation_csvfile(csv_file):
    csv_reader = csv.reader(csv_file, delimiter=",")
    observations = [Observation(*row) for row in csv_reader]
    return observations
