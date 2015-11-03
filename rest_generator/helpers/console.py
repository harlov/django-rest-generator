class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_common(inp, clr):
	print(clr+inp+bcolors.ENDC)

def print_ok(inp):
	print_common(inp, bcolors.OKGREEN)

def print_fail(inp):
	print_common(inp, bcolors.FAIL)

def print_bold(inp):
	print_common(inp, bcolors.BOLD)