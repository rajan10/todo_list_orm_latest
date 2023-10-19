def requires_numeric_option(fxn):
    def inner(*args):
        option = fxn(*args)
        if option.isnumeric():  
            return int(option)
        raise ValueError("Pls. enter numeric value")

    return inner
