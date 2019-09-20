from pkg_resources import DistributionNotFound, get_distribution

try:
    __version__ = get_distribution(__package__).version
    version = __version__
except DistributionNotFound:
    # package is not installed
    pass
