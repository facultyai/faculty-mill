from pkg_resources import get_distribution, DistributionNotFound

try:
    __version__ = get_distribution(__name__).version
except DistributionNotFound:
    # package is not installed
    pass


version = __version__


def print_version(ctx, param, value):
    if not value:
        return

    print(version)
    ctx.exit()
