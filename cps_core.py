import argparse
import os,sys,csv
from subprocess import *


class mapping:
    def __init__(self):
        self.bowtie2_build = 'bowtie2-build'
        self.bowtie2 = 'bowtie2'
        self.samtools = 'samtools'
        self.bedtools = 'bedtools'
        self.spades = 'spades.py'

    def run(self, cmd, wkdir=None):
        sys.stderr.write("Running %s ...\n" % cmd)
        p = Popen(cmd, shell=True, cwd=wkdir)
        p.wait()
        return p.returncode

    def make_index(self, ref_genome, ref_index):
        cmd = '%s -f %s %s' % (self.bowtie2_build, ref_genome, ref_index)
        return cmd

    def alignment(self, ref_index, fq_1, fq_2, sam, log):
        cmd = '%s -x %s -1 %s -2 %s -S %s 2>%s' % (self.bowtie2, ref_index, fq_1, fq_2, sam, log)
        return cmd

    def sam2bam(self, sam, bam):
        cmd = '%s view -b %s >%s' % (self.samtools, sam, bam)
        return cmd

    def pair_mapped(self, bam, pair_mapped_bam):
        cmd = '%s view -bF 12 %s >%s' % (self.samtools, bam, pair_mapped_bam)
        return cmd

    def bam2fastq(self,pair_mapped_bam,fq1,fq2):
        cmd = '%s bamtofastq -i %s -fq %s -fq2 %s' % (self.bedtools, pair_mapped_bam, fq1, fq2)
        return cmd

    def spades_index(self, fq1, fq2, result):
        cmd = '%s --pe1-1 %s --pe1-2 %s --cov-cutoff auto -t 16 --isolate -o %s' % (self.spades, fq1, fq2, result)
        return cmd

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="DNA persentage")
    parser.add_argument("-rg", "--ref_genome", required=True, type=str, help="Reference genome")
    parser.add_argument("-fq1", "--fq_1", required=True, type=str, help="Input Fastq1")
    parser.add_argument("-fq2", "--fq_2", required=True, type=str, help="Input Fastq2")
    Args = parser.parse_args()

    mp = mapping()
    nam = os.path.basename(Args.fq_1)
    name = nam.split('_')[0]
    path = os.path.dirname(Args.ref_genome)
    genome = os.path.basename(Args.ref_genome)
    index = genome.split('.')[0]
    fq_1 = Args.fq_1
    fq_2 = Args.fq_2

    os.chdir(path)

    if os.path.exists('./' + name):
        pass
    else:
        os.mkdir('./' + name)

    if os.path.exists('./' + name + '/index'):
        pass
    else:
        os.mkdir('./' + name + '/index')

    cmd_1 = mp.make_index(genome,'./' + name + '/index/' + index)
    mp.run(cmd=cmd_1)

    sam = name + '.sam'
    cmd_2 = mp.alignment('./' + name + '/index/' + index, fq_1, fq_2, './' + name + '/' + sam, './' + name + '/log')
    mp.run(cmd=cmd_2)

    bam = name + '.bam'
    cmd_3 = mp.sam2bam('./' + name + '/' + sam, './' + name + '/' + bam)
    mp.run(cmd=cmd_3)

    pair_bam = name + '_pair.bam'
    cmd_4 = mp.pair_mapped('./' + name + '/' + bam,
                           './' + name + '/' + pair_bam)
    mp.run(cmd=cmd_4)

    pair_fq1 = name + '_pair-1.fq'
    pair_fq2 = name + '_pair-2.fq'
    cmd_5 = mp.bam2fastq('./' + name + '/' + pair_bam,
                         './' + name + '/' + pair_fq1,
                         './' + name + '/' + pair_fq2)
    mp.run(cmd=cmd_5)

    result = 'result_' + name
    cmd_6 = mp.spades_index('./' + name + '/' + pair_fq1,
                         './' + name + '/' + pair_fq2,
                         './' + name + '/' + 'result_' + name)
    mp.run(cmd=cmd_6)

    if os.path.exists('./' + name + '/' + 'result_' + name + '/scaffolds.fasta'):
        os.system('cp %s %s' % ('./' + name + '/' + 'result_' + name + '/scaffolds.fasta',
                                './' + name + '/'))
        os.rename('./' + name + '/scaffolds.fasta',
                  './' + name + '/' + name + '.fasta')

    else:
        if os.path.exists('./' + name + '/' + 'result_' + name + '/contigs.fasta'):
            os.system('cp %s %s' % ('./' + name + '/' + 'result_' + name + '/contigs.fasta',
                                    './' + name + '/'))
            os.rename('./' + name + '/contigs.fasta',
                      './' + name + '/' + name + '.fasta')
        else:
            pass


    os.remove('./' + name + '/' + sam)
    os.remove('./' + name + '/' + bam)
    os.remove('./' + name + '/' + pair_bam)
    os.remove('./' + name + '/' + pair_fq1)
    os.remove('./' + name + '/' + pair_fq2)
    os.system('rm -r %s' % ('./' + name + '/' + 'result_' + name))