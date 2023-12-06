# def get_version() -> str:
#     """Obtain version information from git if available otherwise use
#     the internal version number
#     """

#     def internal_version():
#         return ".".join(map(str, __version_info__[:3])) + "".join(__version_info__[3:])

#     try:
#         p = run(["git", "describe", "--tags"], stdout=PIPE, stderr=DEVNULL, text=True)
#     except FileNotFoundError:
#         return internal_version()

#     if p.returncode:
#         return internal_version()
#     else:
#         return p.stdout.strip()
# __version_info__ = (1, 1, 0, "+git")
# __version__: str = get_version()

__version__ = "0.1.0"
