TISSUE_GENE_PAIRS = [ ['SDHB','Blood'], ['SDHB','Brain'] ]
GENES = set([p[0] for p in TISSUE_GENE_PAIRS])
TISSUES = set([p[1] for p in TISSUE_GENE_PAIRS])

rule all:
    input:
        '_'.join( ['-'.join(p) for p in TISSUE_GENE_PAIRS]) + '.png'

rule plot:
    input:
        expand("{gene}_counts.txt", gene=GENES),
        expand("{tissue}_samples.txt", tissue=TISSUES),
    output:
        '_'.join( ['-'.join(p) for p in TISSUE_GENE_PAIRS]) + '.png'
    shell:
        'python hist.py ' \
        + ' '.join([' '.join(p) for p in TISSUE_GENE_PAIRS]) \
        + ' {output}'


rule tissue_samples:
    input:
        "GTEx_Analysis_v8_Annotations_SampleAttributesDS.txt"
    output:
        expand("{tissue}_samples.txt", tissue=TISSUES)
    shell:
        "for tissue in {TISSUES}; do " \
        +  "python get_tissue_samples.py {input} $tissue $tissue\_samples.txt;"\
        + "done"

rule sample_tissue_data:
    output:
        "GTEx_Analysis_v8_Annotations_SampleAttributesDS.txt"
    shell:
        "wget https://storage.googleapis.com/gtex_analysis_v8/annotations/GTEx_Analysis_v8_Annotations_SampleAttributesDS.txt"

rule gene_sample_counts:
    input:
        "GTEx_Analysis_2017-06-05_v8_RNASeQCv1.1.9_gene_reads.acmg_59.gct.gz"
    output:
        expand("{gene}_counts.txt", gene=GENES)
    shell:
        "for gene in {GENES}; do " \
        +   "python get_gene_counts.py {input} $gene $gene\_counts.txt;" \
        + "done"
        
rule gene_data:
    output:
        "GTEx_Analysis_2017-06-05_v8_RNASeQCv1.1.9_gene_reads.acmg_59.gct.gz"
    shell:
        "wget https://github.com/swe4s/lectures/raw/master/data_integration/gtex/GTEx_Analysis_2017-06-05_v8_RNASeQCv1.1.9_gene_reads.acmg_59.gct.gz"

