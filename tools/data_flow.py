


def auto_type_conv(val:str or list):
    """ Convert str to the proper data type
    """
    if type(val) == list:
        return [auto_type_conv(v) for v in val]

    if type(val) != str: # already converted
        return val
        
    elif any(v.isalpha() for v in val): # '12x' or 'ab'
        return val

    elif '.' in val: 
        return float(val)
    else:
        return int(val)


def parse_config_file(text:str) -> dict:
    """conver config text to dict
    ex:
    text = 
    '
        # Config commant
        a = 1  # line commant
        # another commant
        b = [1,4]
    '
    return {'a':1, 'b':[1,4]}
    """
    
    config_dict = {}
    for line in text.split('\n'):
        if line.startswith("#") or "=" not in line: #This is valued for header only
            continue # skip comments
        end = line.find('#') 
        if end == -1:
            end = None 
        line = line[ : end].replace(' ', '')
        key, value = line.split("=")
        if value.startswith("[") or "," in value:
            value = value.replace("[",'').replace("]", '')
            if ',' in value:
                value = value.split(",")
                if not value[-1]: # ["abc",""]
                    value = value[:-1]
            else:
                value = [value]
        config_dict[key] = value
    return config_dict


def header_to_dict(file_str):
    """ Parse data (.txt) filse heasers to dict
    """
    hd = {}
    for line in file_str.split('\n'):
        if line.startswith("#") and ":" in line:
            line = line.replace('# ','').replace('\r','')
            parts = line.split(":")
            key = parts[0]
            if len(parts) == 2:
                value = parts[1]
            else:
                value = ' '.join(parts[1:])
            hd[key] = value
        else: #This is valued for header only
            return hd