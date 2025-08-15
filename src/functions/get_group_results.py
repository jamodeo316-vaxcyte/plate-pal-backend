import pandas as pd
import numpy as np

from cloud_models import AzureModel


def get_group_results(data):
    plate_values, plate_map = data['plate_values'], data['plate_map']
    sample_names = list(pd.unique(plate_map.values.ravel()))
    sample_names.remove('N/A')

    dilution_extractor_prompt = f"""
    I am running a plate-based assay to determine the concentration isolated proteins.
    Review this list of sample names found in my plate map: {str(sample_names)}.
    Determine the dilution factor of each sample based on its name (e.g., 6 for '1:6 DF FimA Lot #: KW-347-073').
    If a dilution factor cannot be determined, default to 1.
    ONLY return these dilution factors, separated by commas.
    Ensure they are in the same order as the list of sample names.
    Do NOT include code fences, prose, or additional output of *any* kind.
    """

    dilution_extractor = AzureModel("gpt-4o")
    messages = [{"role": "user", "content": dilution_extractor_prompt}]
    dilution_factors = dilution_extractor.get_response(messages)
    dilution_factors = [float(factor.strip()) for factor in dilution_factors.split(',')]

    sample_indicies = []
    for name in sample_names:
        filter = (plate_map == name)
        indicies = list(zip(*filter.to_numpy().nonzero()))
        sample_indicies.append(indicies)

    sample_values = []
    for indicies in sample_indicies:
        values = []
        for loc in indicies:
            value = float(plate_values.iloc[loc])
            values.append(value)
        sample_values.append(values)

    group_results = {}
    for i, name in enumerate(sample_names):
        values = sample_values[i]
        dilution = dilution_factors[i]
        mean = np.mean(values)
        std = np.std(values)
        rstd = (std / mean) * 100 if mean != 0 else 0

        group_results[name] = {
            'values': values,
            'dilution': dilution,
            'mean': mean,
            'std': std,
            'rstd': rstd
        }

    data['group_results'] = group_results
    
    return data
