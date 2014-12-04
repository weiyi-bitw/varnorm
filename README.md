variant normalization toolkit
=============

Normalize variants in VCF file using left-aligned normalization. Basically a wrapper around Counsyl's hgvs package.

Prerequiesite
-------------

Setup $HG19 environment variable.

python packages:
- hgvs from [Counsyl](https://github.com/counsyl/hgvs)
- pygr

normVCF
-------

Normalize variants in a VCF file.

```shell
$ normVCF -h
usage: normVCF [-h] [-o OUTPUT_FILE] [--reference REF_GENOME] [-v] [--novkey]
               [-s]
               INPUT_FILE

positional arguments:
  INPUT_FILE            Input text file to load into database.

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT_FILE, --output OUTPUT_FILE
                        Output file. Default: stdout
  --reference REF_GENOME
                        Path to reference genome .fa file. Default: $HG19
                        environmental variable.
  -v, --verbose         Run in verbose mode.
  --novkey              Do not generate vkey.
  -s, --sample          Keep sample information.

```

###Usage example:

```shell

#check for packages installed
(env) $ pip freeze
argparse==1.2.1
hgvs==0.8
pygr==0.8.2
varnorm==0.2
wsgiref==0.1.2

#check for environment variable $HG19
#can also be passed by --reference argument
(env) $ echo $HG19
/path/to/your/hg19.fa

#run simple test
(env) $ normVCF data/test.vcf -o testout.vcf

```



