from cloud_models import AzureModel


def get_file_information(raw_data):
    raw_data = raw_data.to_csv()

    extractor_prompt = f"""
    Review the raw instrument file from a plate reader below:
    {raw_data}

    One of the cells contains a string of file information in the following format:
    "Original Filename: 2024-02-27 Raw Data; Date Last Saved: 2/27/2024 1:04:29 PM"

    ONLY return this string.
    Do NOT include code fences, prose, or additional output of *any* kind.
    """

    extractor = AzureModel("gpt-4o")
    messages = [{"role": "user", "content": extractor_prompt}]
    file_info = extractor.get_response(messages)

    return file_info
