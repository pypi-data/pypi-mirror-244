#
#  This file is part of Sequana software
#
#  Copyright (c) 2016-2022 - Sequana Development Team
#
#  Distributed under the terms of the 3-clause BSD license.
#  The full license is in the LICENSE file, distributed with this software.
#
#  website: https://github.com/sequana/sequana
#  documentation: http://sequana.readthedocs.io
#
##############################################################################
from collections import defaultdict

import colorlog
from sequana.fasta import FastA
from sequana.gff3 import GFF3
from tqdm import tqdm
logger = colorlog.getLogger(__name__)
import pandas as pd



class KOZAK:
    """

    k = KOSAC()
    odds = k.get_odd_ratio()
    fitter(odds)


    exponweib
    betaprime
    f
    johnsonsu
    invgauss

    List of most common sequences


    Filter only to keep ATG since others seems to ncRNA

    - raw KOZAK sequence names and counts
    - a KOZAK is e.g GGCRGG  . first position is the less important

    - for the enueration of kmers, get of the rid of the Ns

    - odds ratio have 4 cases depending on the on enumeration:
        use entire genome
        use chromosome by chromosome
        use of gene on genome
        use gene on chromosomes


    Table of counts of Kozak sequences without dna ambiguities.
    - across the entire genome
    - by chromosomes

    """
    def __init__(self, fasta, gff, genetic_type="gene"):
        self.fasta = FastA(fasta)
        self.gff = GFF3(gff)
        self.genetic_type = genetic_type

    def get_all_kmer_counts_by_chromosome(self, k):
        counts = {}

        for chrom, sequence in tqdm(zip(self.fasta.names, self.fasta.sequences)):
            count = defaultdict(int)
            for i in range(0, len(sequence) - k + 1):
                count[sequence[i : i + k]] += 1
            counts[chrom] = count
        return counts

    def get_chromosome(self, chrom_name=None, genetic_type="gene"):
        count = defaultdict(int)
        for chrom, sequence in zip(self.fasta.names, self.fasta.sequences):

            starts = self.gff.df.query("genetic_type==@genetic_type and seqid==@chrom").start

            for start in starts:
                count[sequence[start-1-6:start+6-1-6]]+=1
        df = pd.DataFrame(count.items())
        df.columns = ["kmer", "counts"]
        df = df.sort_values("counts", ascending=False)
        df = df.reset_index(drop=True)
        return df

    def get_all_kmers_normalised(self, k=6):

        kmers = self.get_all_kmer_counts_by_chromosome(k=k)
        kmers = pd.DataFrame(kmers)
        #kmers = kmers.divide(self.fasta.get_lengths_as_dict())*1000000
        return kmers

    def get_odd_ratio(self):

        df = self.get_chromosome()
        kmers = self.get_all_kmers_normalised()

        Ngenes = 10000
        genome_size = 33e6

        #df = df.query("counts > 20")

        odds = []
        for k, row in df.iterrows():
            row.counts
            A = row.counts / Ngenes
            B = kmers.loc[row.kmer].sum() / genome_size
            print(row.counts, row.kmer, A, B, A/B)
            odds.append(A / B)
        return odds



