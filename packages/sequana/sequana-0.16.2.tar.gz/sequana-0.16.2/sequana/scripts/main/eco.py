#  This file is part of Sequana software
#
#  Copyright (c) 2016-2020 - Sequana Development Team
#
#  Distributed under the terms of the 3-clause BSD license.
#  The full license is in the LICENSE file, distributed with this software.
#
#  website: https://github.com/sequana/sequana
#  documentation: http://sequana.readthedocs.io
#
##############################################################################

import pandas as pd
import os

from sequana.modules_report import ModuleKEGGEnrichment

log2FC = 1


taxon = "eco"

params  = params={
             "padj": 0.05,
             "log2_fc": log2FC,
             "nmax": 15,
             "max_entries": 3000,
             "kegg_background": 4600,
             "mapper": None,
             "preload_directory": "local",
             "color_node_with_annotation": "Name",
            "plot_logx": True,
         }

if os.path.exists("local") is False:
    os.makedirs("local", exist_ok=True)
if os.path.exists("local/eco.json") is False:
    params["preload_directory"] = None

df = pd.read_excel("B17473.xlsx", sheet_name="SHB- Transcriptomics")
df.columns = ["Name", "log2FoldChange", "logCPM", "F", "PValue", "padj"]


#df = pd.read_csv("test.csv")
gene_dict = {}
gene_dict["up"] = list(df.query("log2FoldChange>@log2FC and padj<0.05").Name.values)
gene_dict["down"] = list(df.query("log2FoldChange<-@log2FC and padj<0.05").Name.values)
gene_dict["all"] = list(df.query("(log2FoldChange<-@log2FC or log2FoldChange>@log2FC) and padj<0.05").Name.values)


m = ModuleKEGGEnrichment(
    gene_dict,
    taxon,
    df,
    enrichment_params=params,
    used_genes=None,
    )

m.ke.save_pathways("local")

