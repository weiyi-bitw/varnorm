import sys
import copy
import gzip
from varcharkey import VarCharKey
from hgvs import *
from pygr.seqdb import SequenceFileDB

class VCFNormalization(object):
    
    def __init__(self, inFile, genome, vkey = False, verbose=False, log=sys.stderr):
        self.inFile = inFile
        self.verbose = verbose
        self.log = log
        self.vkey=vkey
        self.genome = SequenceFileDB(genome)
        self.infoHeader = "[" + self.__class__.__name__ + "]"

    def info(self, message):
        if self.verbose:
            print >> self.log, self.infoHeader + message

    def normAVar(self, chrom, start, end, ref, alt):
        if not ref:
            ref = str(self.genome['chr'+chrom][(start-1):end]).upper()
        if ref == '.' or ref == '-':
            start -= 1
            ref = str(self.genome['chr'+chrom][start-1]).upper()
            alt = ref + alt
        elif alt == '.' or alt == '<DEL>' or alt == '-':
            start -= 1
            prefix = str(self.genome['chr'+chrom][start-1]).upper()
            ref = prefix+ref
            alt = prefix

        nv = normalize_variant('chr' + chrom, start, ref, [alt], self.genome)
        ref_norm = nv.ref_allele
        alt_norm = nv.alt_alleles[0]
        start_norm = nv.position.chrom_start
        end_norm = start_norm + len(ref_norm) - 1
        return chrom, start_norm, end_norm, ref_norm, alt_norm

    def parse_line_nosample(self, line):
        if line.startswith('#'):
            return [line.strip()]
        tokens = line.strip().split('\t')

        chrom = tokens[0].replace('chr', '')
        pos = int(tokens[1])
        varID = tokens[2]
        ref = tokens[3]
        alts = tokens[4].split(',')
        nalts = len(alts)

        out = []

        for a in range(nalts):
            alt = alts[a]
            
            tk = copy.deepcopy(tokens)

            if ref == '.':
                pos -= 1
                ref = str(self.genome['chr'+chrom][pos-1]).upper()
                alt = ref + alt
            elif alt == '.' or alt == '<DEL>':
                pos -= 1
                prefix = str(self.genome['chr'+chrom][pos-1]).upper()
                ref = prefix+ref
                alt = prefix

            nv = normalize_variant('chr'+chrom, pos, ref, [alt], self.genome)
            ref_norm = nv.ref_allele
            alt_norm = nv.alt_alleles[0]
            start_norm = nv.position.chrom_start
            end_norm = start_norm + len(ref_norm) - 1
            
            if self.vkey:
                vk = VarCharKey.v2k(chrom, start_norm, end_norm, alt_norm)
                if vk != None:
                    info = tk[7]
                    if info == '.':
                        info = "VKEY=" + vk
                    else:
                        info = "VKEY=" + vk + ";" + info
                    tk[7] = info

            tk[:5] = [chrom, str(start_norm), varID, ref_norm, alt_norm]

            out.append("\t".join(tk[:8]))

        return out

    def parse_line(self, line):
        if line.startswith('#'):
            return [line.strip()]
        tokens = line.strip().split('\t')

        chrom = tokens[0].replace('chr', '')
        pos = int(tokens[1])
        varID = tokens[2]
        ref = tokens[3]
        alts = tokens[4].split(',')
        nalts = len(alts)

        out = []

        for a in range(nalts):
            alt = alts[a]
            
            tk = copy.deepcopy(tokens)

            if ref == '.':
                pos -= 1
                ref = str(self.genome['chr'+chrom][pos-1]).upper()
                alt = ref + alt
            elif alt == '.' or alt == '<DEL>':
                pos -= 1
                prefix = str(self.genome['chr'+chrom][pos-1]).upper()
                ref = prefix+ref
                alt = prefix

            nv = normalize_variant('chr'+chrom, pos, ref, [alt], self.genome)
            ref_norm = nv.ref_allele
            alt_norm = nv.alt_alleles[0]
            start_norm = nv.position.chrom_start
            end_norm = start_norm + len(ref_norm) - 1
            
            if self.vkey:
                vk = VarCharKey.v2k(chrom, start_norm, end_norm, alt_norm)
                if vk != None:
                    info = tk[7]
                    if info == '.':
                        info = "VKEY=" + vk
                    else:
                        info = "VKEY=" + vk + ";" + info
                    tk[7] = info

            tk[:5] = [chrom, str(start_norm), varID, ref_norm, alt_norm]

            out.append("\t".join(tk))

        return out

    def run(self, out=sys.stdout, keepSample=True):
        parse_line = self.parse_line_nosample
        if keepSample:
            parse_line = self.parse_line
        fi = gzip.open(self.inFile, 'rb') if self.inFile.endswith('gz') else open(self.inFile, 'rb')
        for line in fi:
            too = parse_line(line)
            for t in too:
                print >> out, t
                    
        

