import numpy as np
from scipy import stats

from cloud_models import AzureModel


def fit_standard_curve(data):
    group_results = data['group_results']
    sample_names = str(list(group_results.keys()))

    name_extractor_prompt = f"""
    I am running a plate-based assay to determine the concentration isolated proteins.
    Review this list of sample names found in my plate map: {sample_names}.
    Determine which names indicate samples containing a protein standard (e.g., BSA Std).
    ONLY return these names, separated by commas.
    Do NOT include code fences, prose, or additional output of *any* kind.
    """

    name_extractor = AzureModel("gpt-4o")
    messages = [{"role": "user", "content": name_extractor_prompt}]
    standard_names = name_extractor.get_response(messages)
    standard_names = [name.strip() for name in standard_names.split(',')]

    absorbance_means = []
    for name in standard_names:
        mean = group_results[name]['mean']
        absorbance_means.append(mean)
    absorbance_means = np.array(absorbance_means)

    concentration_extractor_prompt = f"""
    I am running a plate-based assay to determine the concentration isolated proteins.
    Review this list of protein standard names found in my plate map: {standard_names}.
    Determine the concentrations of each standard based on its name (e.g., 25 ug/mL BSA Std).
    ONLY return the concentration numerical values, separated by commas.
    Ensure they are in the same order as the list of protein standard names.
    Do NOT include code fences, prose, or additional output of *any* kind.
    """

    concentration_extractor = AzureModel("gpt-4.1-nano")
    messages = [{"role": "user", "content": concentration_extractor_prompt}]
    standard_concentrations = concentration_extractor.get_response(messages)
    standard_concentrations = [float(value.strip()) for value in standard_concentrations.split(',')]
    standard_concentrations = np.array(standard_concentrations)

    slope, intercept, r_value, p_value, std_err = stats.linregress(standard_concentrations, absorbance_means)
    curve_fit = {
        "slope": slope,
        "intercept": intercept,
        "r_squared": r_value ** 2,
        "p_value": p_value,
        "std_err": std_err,
        "standard_names": standard_names,
        "x_values": standard_concentrations,
        "y_values": absorbance_means
    }

    data['curve_fit'] = curve_fit

    return data
