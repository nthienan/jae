
def str_to_megabytes(raw_data):
    arr = raw_data.split(" ")
    if arr[1].strip().lower() == "bytes":
        return float(arr[0]) / 1000000
    if arr[1].strip().lower() == "kb":
        return float(arr[0]) / 1000
    if arr[1].strip().lower() == "mb":
        return float(arr[0])
    if arr[1].strip().lower() == "gb":
        return float(arr[0]) * 1000
    if arr[1].strip().lower() == "tb":
        return float(arr[0]) * 1000000


def str_to_int(raw_data):
    return int(raw_data.replace(",", ""))
