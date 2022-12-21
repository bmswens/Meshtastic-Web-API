
def clean_position(position):
    """Returns a JSON serializable 'position' object."""
    output = dict(**position)
    if output.get('raw'):
        del output['raw']
    return output