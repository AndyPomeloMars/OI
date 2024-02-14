def list_like(data):
    return isinstance(data, tuple) or isinstance(data, list)

def basicdt_like(data):
    return isinstance(data, int) or isinstance(data, float) or isinstance(data, str) or isinstance(data, bool)

def args_to_list(*args, data = []):
    for element in args:
        if list_like(element):
            for include_element in element:
                args_to_list(include_element, data = data)
        else:
            data.append(str(element))

    return data
