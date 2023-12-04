
def by_dest_metavar_and_prefix_char(dest, metavar, prefix_char):
    if metavar is str:
        dest = metavar
    else:
        dest = str(dest)
    if len(dest) < 1:
        raise ValueError
    if len(dest) == 1:
        prefix = "_"
    else:
        prefix = "__"
    ans = prefix + dest
    ans = ans.replace('_', prefix_char)
    return ans