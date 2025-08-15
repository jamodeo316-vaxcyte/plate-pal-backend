

def get_concentrations(data):
    plate_values, curve_fit = data['plate_values'], data['curve_fit']
    m = curve_fit['slope']
    b = curve_fit['intercept']

    def calculate_concentration(y):
        x = (y - b) / m
        return x

    concentrations = plate_values.apply(calculate_concentration)
    data['concentrations'] = concentrations

    return data
    