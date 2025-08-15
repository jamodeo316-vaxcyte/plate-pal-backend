from cloud_models import AzureModel


def get_results_summary(data):
    results_table, curve_fit = data['results_table'], data['curve_fit']
    results_table = results_table.to_csv()
    standard_names = str(curve_fit['standard_names'])
    r_squared = str(curve_fit['r_squared'])

    results_summarizer_prompt = f"""
    Summarize the bicinchoninic acid (BCA) assay results shown in the table below:
    {results_table}

    A standard curve was made via linear regression (mean absorbance vs. concentration) using these standards:
    {standard_names}

    Comment on the standard curve fit based on the following r-squared value:
    {r_squared}

    Indicate whether all RSDs were < 5%, and list any samples with RSD > 5%.
    Comment on the yield of the proteins isolated in the non-standard sample (high, medium, low).
    Note any other trends or insights you observe.
    Include a final conclusion on the reliability and precision of the data.
    Format your summary as a concise single paragraph.
    Do NOT include code fences, prose, or additional output of *any* kind.
    """

    results_summarizer = AzureModel("gpt-4o")
    messages = [{"role": "user", "content": results_summarizer_prompt}]
    results_summary = results_summarizer.get_response(messages)

    data['results_summary'] = results_summary

    return data
