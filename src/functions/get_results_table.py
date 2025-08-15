import pandas as pd


def get_results_table(data):
    group_results, concentrations, plate_map = data['group_results'], data['concentrations'], data['plate_map']
    
    
    results_table = []
    for group, result in group_results.items():
        values = result['values']
        row = {
            "Sample Label": group,
            "Absorbance Values": str(values),
            "Number of Replicates": len(values),
            "Mean Absorbance": round(result['mean'], 4),
            "Std. Dev": round(result['std'], 3),
            "RSD (%)": round(result['rstd'], 2),
            "Dilution Factor": round(result['dilution'], 1)
        }
        results_table.append(row)

    results_table = pd.DataFrame(results_table)
    results_table = results_table.sort_values(by='Mean Absorbance', ascending=True)
    data['results_table'] = results_table

    return data
