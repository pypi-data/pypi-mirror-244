import pandas as pd

from pylab import plot


import numpy as np


class ATAC:
    def __init__(self):
        print("reading test_treat_pileup")

        self.pileup = pd.read_csv("test_treat_pileup.bdg", sep="\t", header=None)
        self.pileup.columns = ["name", "start", "stop", "count"]
        self.pileup = self.pileup.query("name=='22'")

        self.CT = pd.read_csv("CTCF_chr22.bed", sep="\t", header=None)
        self.CT.columns = ["name", "start", "stop", 4, 5, 6, 7, 8, 9, 10]

        # Let us assume TSS is the start of self.CT entries.
        # we compute the coverage  +- 1kb  around the TSS

    def plot_peaks(self, position, side_window=1000):
        data = self.pileup.query("start<@position+@side_window and stop>@position-@side_window")

        coverage = np.zeros(2 * side_window + 1)
        for x, y, z in zip(data.start, data.stop, data["count"]):
            coverage[x - position + side_window : y - position + side_window] += float(z)
        return coverage
