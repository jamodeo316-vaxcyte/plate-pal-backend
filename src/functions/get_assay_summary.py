

def get_assay_summary(data):
    assay_summary = """
    The Bicinchoninic Acid (BCA) assay is a colorimetric method for quantifying total protein concentration in biological samples.
    The assay is based on a two-step reaction.
    First, under alkaline conditions, peptide bonds in proteins reduce cupric ions (Cu2+) to cuprous ions (Cu+) in a biuret-like reaction.
    Second, the generated Cu+ ions form an intense purple-colored complex with bicinchoninic acid.
    This complex exhibits a strong absorbance at 562 nm, which is directly proportional to the protein concentration over a broad dynamic range (typically 20 µg/mL to 2 mg/mL).
    The BCA assay is compatible with many detergents and reducing agents, offers high sensitivity, and is well suited for high-throughput formats.
    """

    data['assay_summary'] = assay_summary

    return data
