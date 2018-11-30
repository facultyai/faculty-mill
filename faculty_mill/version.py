__version__ = "0.0.1"
version = __version__


def print_version(ctx, param, value):
    if not value:
        return

    print(version)
    ctx.exit()
