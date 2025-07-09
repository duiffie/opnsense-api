import argparse

def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', '1'):
        return True
    elif v.lower() in ('no', 'false', '0'):
        return False
    raise argparse.ArgumentTypeError('Boolean waarde verwacht (true/false)')
