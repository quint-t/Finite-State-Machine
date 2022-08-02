class __EpsilonClass:
    __slots__ = ()

    __INSTANCE = None

    def __new__(cls, *args, **kwargs):
        if cls.__INSTANCE is None:
            cls.__INSTANCE = super().__new__(cls)
        return cls.__INSTANCE

    def __eq__(self, other):
        return (other.lower() if isinstance(other, str) else other) in ('ε', 'epsilon')

    def __contains__(self, other):
        return other == self

    def __str__(self):
        return 'epsilon'  # 'ε'

    def __repr__(self):
        return 'epsilon'


Epsilon = __EpsilonClass()
