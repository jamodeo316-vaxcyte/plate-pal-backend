

def get_plate_values(raw_data):
    plate_values = raw_data.iloc[17:25, 2:14].copy()
    plate_values = plate_values.reset_index(drop=True)
    plate_values.columns = list(range(1, 13))

    return plate_values
    