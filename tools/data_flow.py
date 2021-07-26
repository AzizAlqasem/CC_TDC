


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