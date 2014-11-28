class User:
    """TODO"""
    def __init__(self, name, share_index):
        self.name = name
        self.share_index = share_index

    def __str__(self):
        return 'User({0}, {1})'.format(self.name, self.share_index)
