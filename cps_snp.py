import argparse
import os,sys,csv
from subprocess import *


class mapping:
    def __init__(self):
        self.bowtie2_build = 'bowtie2-build'
        self.bowtie2 = 'bowtie2'
        self.samtools = 'samtools'
        self.freebayes = 'freebayes'

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

    def call_vcf(self, genome, bam, vcf):
        cmd = '%s -f %s %s > %s' % (self.freebayes, genome, bam, vcf)
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

    vcf = name + '.vcf'
    cmd_4 = mp.call_vcf(genome, './' + name + '/' + bam, './' + name + '/' + vcf)
    mp.run(cmd=cmd_4)

    os.remove('./' + name + '/' + sam)
    os.remove('./' + name + '/' + bam)