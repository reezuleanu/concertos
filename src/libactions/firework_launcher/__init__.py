from .launch import launch, delayed_launch

# add any functions and their proper name to this dict
# this dict will be used by the server when converting command data
# from the front end to python code
funcs = {"launch": launch, "delayed_launch": delayed_launch}
