""" Configuration related classes. """

class Config(dict):
    """ Configuration. """

    def __init__(self, **kwargs):
        super(Config, self).__init__(**kwargs)
        self['help'] = False  # help message
        self['no_asserts'] = False  # ignore asserts if true
        self['no_ignore_primitives'] = False  # hide primitives if true
        self['no_anonymize'] = False  # anomyze variables if true
        self['no_ident'] = False  # ignore identation if true
        self['no_getattr'] = False  # ignore getattr calls if true
        self['no_compare'] = False  # ignore compare symbols if true
        self['no_callfunc'] = False  # ignore call function symbols if true
        self['acceptempty'] = False  # accept empty files if true
