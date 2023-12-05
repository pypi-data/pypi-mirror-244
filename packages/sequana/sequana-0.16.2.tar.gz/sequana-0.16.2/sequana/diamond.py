#  This file is part of Sequana software
#
#  Copyright (c) 2016-2021 - Sequana Development Team
#
#
#  Distributed under the terms of the 3-clause BSD license.
#  The full license is in the LICENSE file, distributed with this software.
#
#  website: https://github.com/sequana/sequana
#  documentation: http://sequana.readthedocs.io
#
##############################################################################
import os
import sys
import shutil

from easydev import execute

from sequana.lazy import pandas as pd
from sequana.lazy import pylab
from sequana.lazy import numpy as np


from colormap import Colormap

import colorlog

logger = colorlog.getLogger(__name__)


__all__ = [
    "DiamondResults",
    "DiamondAnalysis",
]


class DiamondResults(object):
    """Translate Diamond results into a Krona-compatible file

    Expect the diamond results to be parsed with daa2info as follows::

        daa2info --in DATA.daa  -o ccc -c2c Taxonomy   -p -r  -m -mro --help

    ::

        k = DiamondResults("diamond.out")
        k.diamond_to_krona()

    The format expected looks like::


    D	[D] Bacteria;	45268.0
    G	[D] Bacteria; [P] Bacteroidetes; [C] Cytophagia; [O] Cytophagales; [F] Spirosomaceae; [G] Runella;	40.0
    G	[D] Bacteria; [P] Bacteroidetes; [C] Cytophagia; [O] Cytophagales; [F] Cytophagaceae; [G] Spirosoma;	123.0
    G	[D] Bacteria; [P] Bacteroidetes; [C] Flavobacteriia; [O] Flavobacteriales; [F] Flavobacteriaceae; [G] Flavobacterium;	449.0


    """

    def __init__(self, filename_taxon="diamond.taxon", filename_path="diamond.path", verbose=True):
        """.. rubric:: **constructor**

        :param filename: the input from DiamondAnalysis class

        """
        self.filename_taxon = filename_taxon
        self.filename_path = filename_path
        self.filename = "diamond"

        if filename_taxon and filename_path:
            # This initialise the data
            self._parse_data()
            self._data_created = False

    def _parse_data(self):
        taxonomy = {}

        logger.info("Reading diamond data from {}".format(self.filename_taxon))
        # we select only col 0,2,3 to save memory, which is required on very

        self._taxons = pd.read_csv(self.filename_taxon, sep="\t", comment="#", header=None)
        self._taxons.columns = ["rank", "taxon", "count"]
        del self._taxons["rank"]
        self._taxons.set_index("taxon", inplace=True)
        self._taxons = self._taxons.astype(int)
        # self._taxons.sort_values(ascending=False, by='taxon', inplace=True)

        #
        data = {"[D]": [], "[K]": [], "[P]": [], "[C]": [], "[O]": [], "[F]": [], "[G]": [], "[S]": [], "[N]": []}
        counts = []

        iline = 0
        df = pd.DataFrame()

        # this is a very poor parsing.
        # difficuly due to diamond format mixing tabulation, ;
        # for we cannot use pandas. instead, we scan looking for the lineage
        with open(self.filename_path, "r") as fin:
            for line in fin.readlines():
                if line.startswith("#"):
                    pass
                elif line.startswith("-"):  # unclassified
                    iline += 1
                    taxon = -1
                    count = int(float(line.split()[-1].replace(",", "")))
                    for key in data.keys():
                        data[key].append("Unclassified")
                    counts.append(count)
                    self.unclassified = count
                else:
                    iline += 1
                    final_rank, ranks, count = line.split("\t")
                    ranks = ranks.strip(";").split(";")
                    dict_ranks = dict([tuple(x.split(maxsplit=1)) for x in ranks])
                    for key in data.keys():
                        data[key].append(dict_ranks.get(key, ""))
                    counts.append(int(float(count.replace(",", "").strip("\n"))))

        self._df = pd.DataFrame(data)
        self._df["count"] = counts
        self._df["percentage"] = self._df["count"] / self._df["count"].sum() * 100
        self._df.rename(
            {
                "[K]": "kingdom",
                "[P]": "phylum",
                "[D]": "domain",
                "[C]": "class",
                "[O]": "order",
                "[F]": "family",
                "[G]": "genus",
                "[S]": "species",
                "[N]": "name",
            },
            inplace=True,
            axis=1,
        )
        self._df["taxon"] = self.taxons.index
        # domain is not used ?
        self._df = self._df[
            [
                "count",
                "percentage",
                "taxon",
                "domain",
                "kingdom",
                "phylum",
                "class",
                "order",
                "family",
                "genus",
                "species",
                "name",
            ]
        ]

        self._df["kingdom"] = self._df[["domain", "kingdom"]].max(axis=1).values

    def _get_taxons(self):
        try:
            return self._taxons
        except:
            self._parse_data()
            return self._taxons

    taxons = property(_get_taxons)

    def _get_df(self):
        try:
            return self._df
        except:
            self._parse_data()
            return self._df

    df = property(_get_df)

    def diamond_to_csv(self, filename):
        self.df.to_csv(filename, index=False)
        return self.df

    # def diamond_to_json(self, filename, dbname):
    #    try:
    #        self.df.to_json(filename, indent=4, orient="records")
    #    except:
    #        self.df.to_json(filename, orient="records")
    #    return self.df

    def diamond_to_krona(self, output_filename=None, nofile=False):
        """

        :return: status: True is everything went fine otherwise False
        """
        if output_filename is None:
            output_filename = self.filename + ".summary"

        taxon_to_find = list(self.taxons.index)
        if len(taxon_to_find) == 0:
            logger.warning("No reads were identified. You will need a more complete database")
            self.output_filename = output_filename
            with open(output_filename, "w") as fout:
                fout.write("%s\t%s" % (self.unclassified, "Unclassified"))
            return False

        if len(taxon_to_find) == 0:
            return False

        # Now save the file
        self.output_filename = output_filename
        with open(output_filename, "w") as fout:
            for item in self.df.iterrows():
                item = [
                    str(x)
                    for x in item[1][
                        ["count", "kingdom", "phylum", "class", "order", "family", "genus", "species", "name"]
                    ]
                ]
                line = "\t".join(item)
                fout.write(line + "\n")
        self._data_created = True
        return True

    def plot2(self, kind="pie", fontsize=12):
        """This is the simplified static krona-like plot included in HTML reports"""
        import matplotlib.pyplot as plt

        taxons = self.taxons.copy()
        if len(self.taxons.index) == 0:
            return None

        self.dd = self.df.copy()

        df = self.df.copy()
        df["ratio"] = taxons["count"] / taxons["count"].sum() * 100

        data_class = df.groupby(["kingdom", "class"]).sum()
        data_species = df.groupby(["kingdom", "species"]).sum()

        X = []
        Y = []
        Z = []
        labels = []
        zlabels, ztaxons = [], []
        kingdom_colors = []
        inner_colors = []
        inner_labels = []
        species_colors = []
        taxons = df["species"].reset_index().set_index("species")

        for kingdom in data_class.index.levels[0]:
            # kingdom info
            X.append(data_class.loc[kingdom].ratio.sum())

            # class info
            y = list(data_class.loc[kingdom].ratio.values)
            temp = data_class.loc[kingdom]
            y1 = temp.query("ratio>=0.5")
            y2 = temp.query("ratio<0.5")
            y = list(y1.ratio.values) + list(y2.ratio.values)
            inner_labels += list(y1.ratio.index) + [""] * len(y2.ratio)
            Y.extend(y)

            # species info
            temp = data_species.loc[kingdom]
            z1 = temp.query("ratio>=0.5")
            z2 = temp.query("ratio<0.5")
            z = list(z1.ratio.values) + list(z2.ratio.values)
            zlabels += list(z1.ratio.index) + [""] * len(z2.ratio)
            Z.extend(z)

            if kingdom.strip():
                labels.append(kingdom)
            else:
                labels.append("undefined/unknown taxon")

            if kingdom == "Eukaryota":
                this_cmap = plt.cm.Purples
            elif kingdom == "Unclassified":
                this_cmap = plt.cm.Greys
            elif kingdom == "Bacteria":
                this_cmap = plt.cm.Reds
            elif kingdom == "Viruses":
                this_cmap = plt.cm.Greens
            elif kingdom == "Archaea":
                this_cmap = Colormap().cmap_linear("yellow", "yellow", "orange")
            else:
                this_cmap = Colormap().cmap_linear("light gray", "gray(w3c)", "dark gray")

            kingdom_colors.append(this_cmap(0.8))
            inner_colors.extend(this_cmap(np.linspace(0.6, 0.2, len(y))))
            species_colors.extend(this_cmap(np.linspace(0.6, 0.2, len(z))))

        fig, ax = pylab.subplots(figsize=(9.5, 7))
        size = 0.2

        pct_distance = 0
        w1, l1 = ax.pie(
            X,
            radius=1 - 2 * size,
            colors=kingdom_colors,
            wedgeprops=dict(width=size, edgecolor="w"),
            labels=labels,
            labeldistance=0.4,
        )

        w2, l2 = ax.pie(
            Y,
            radius=1 - size,
            colors=inner_colors,
            labels=[x.replace("Unclassified", "") for x in inner_labels],
            wedgeprops=dict(width=size, edgecolor="w"),
            labeldistance=0.65,
        )

        # labels can be long. Let us cut them
        zlabels2 = []
        for this in zlabels:
            if len(this) > 30:
                zlabels2.append(this[0:30] + "...")
            else:
                zlabels2.append(this)

        w3, l3 = ax.pie(
            Z,
            radius=1,
            colors=species_colors,
            labels=[x.replace("Unclassified", "") for x in zlabels2],
            wedgeprops=dict(width=size, edgecolor="w"),
            labeldistance=0.9,
        )

        ax.set(aspect="equal")
        pylab.subplots_adjust(right=1, left=0, bottom=0, top=1)
        pylab.legend(labels, title="kingdom", loc="upper right", fontsize=fontsize)
        import webbrowser

        mapper = {k: v for k, v in zip(zlabels, Z)}

        def on_pick(event):
            wedge = event.artist
            label = wedge.get_label()
            if mapper[label] > 1:
                taxon = taxons.loc[label, "index"]
                webbrowser.open("https://www.ncbi.nlm.nih.gov/Taxonomy/Browser/wwwtax.cgi?id={}".format(taxon))
            else:
                wedge.set_color("white")

        for wedge in w3:
            wedge.set_picker(True)
        fig.canvas.mpl_connect("pick_event", on_pick)

        # this is used to check that everything was okay in the rules
        return df

    def plot(
        self,
        kind="pie",
        cmap="tab20c",
        threshold=1,
        radius=0.9,
        textcolor="red",
        delete_krona_file=False,
        **kargs,
    ):
        """A simple non-interactive plot of taxons

        :return: None if no taxon were found and a dataframe otherwise

        A Krona Javascript output is also available in :meth:`diamond_to_krona`

        .. plot::
            :include-source:

            from sequana import DiamondResults, sequana_data
            test_file = sequana_data("diamond.out", "doc")
            k = DiamondResults(test_file)
            df = k.plot(kind='pie')

        .. seealso:: to generate the data see :class:`DiamondPipeline`
            or the standalone application **sequana_taxonomy**.


        .. todo:: For a future release, we could use this kind of plot
            https://stackoverflow.com/questions/57720935/how-to-use-correct-cmap-colors-in-nested-pie-chart-in-matplotlib
        """
        if len(self._df) == 0:
            return

        if self._data_created == False:
            status = self.diamond_to_krona()

        if kind not in ["barh", "pie"]:
            logger.error("kind parameter: Only barh and pie are supported")
            return
        # This may have already been called but maybe not. This is not time
        # consuming, so we call it again here

        if len(self.taxons.index) == 0:
            return None

        assert threshold > 0 and threshold < 100

        # everything below the threshold (1) is gather together and summarised
        # into 'others'
        data = self.df.copy()
        counts = (self.taxons["count"] / self.taxons["count"].sum() * 100).values
        other_counts = data[counts < threshold].sum()
        data = data[counts >= threshold]

        data.index = data["taxon"]

        if other_counts["count"] > 0:
            data.loc["others"] = [
                other_counts["count"],
                other_counts["percentage"],
                -1,
            ] + ["others"] * 9

        data.sort_values(by="count", inplace=True)

        pylab.figure(figsize=(10, 8))
        pylab.clf()
        self.dd = data
        if kind == "pie":
            ax = data.plot(kind=kind, cmap=cmap, autopct="%1.1f%%", radius=radius, **kargs)
            pylab.ylabel(" ")
            for text in ax.texts:
                #  large, x-small, small, None, x-large, medium, xx-small,
                #  smaller, xx-large, larger
                text.set_size("small")
                text.set_color(textcolor)
            for wedge in ax.patches:
                wedge.set_linewidth(1)
                wedge.set_edgecolor("k")
            self.ax = ax
        elif kind == "barh":
            ax = data.plot(kind=kind, **kargs)
            pylab.xlabel(" percentage ")
        if delete_krona_file:
            os.remove(self.filename + ".summary")

        return data

    def to_js(self, output="krona.html"):
        if self._data_created == False:
            status = self.diamond_to_krona()
        execute("ktImportText %s -o %s" % (self.output_filename, output))
