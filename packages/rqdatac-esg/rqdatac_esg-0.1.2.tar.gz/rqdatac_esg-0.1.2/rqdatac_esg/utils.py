def ensure_list(s, expect_type, name=""):
    if isinstance(s, expect_type):
        return [s]    
    result = list(s)
    for v in result:
        if not isinstance(v, expect_type):
            raise ValueError("{}: expect {!r}, got {!r}".format(name, expect_type, v))
    return result