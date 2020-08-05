import sys

# update_progress() : Displays or updates a console progress bar
## Accepts a float between 0 and 1. Any int will be converted to a float.
## A value under 0 represents a 'halt'.
## A value at 1 or bigger represents 100%
def update_progress(progress, timeleft = 0):
    barLength = 10 # Modify this to change the length of the progress bar
    if timeleft == 0:
        status = ""
    else:
        if timeleft < 120:
            status = "{0} s".format(round(timeleft))
        if timeleft > 120:
            status = "{0} m".format(round(timeleft/60, 1))
        if timeleft > 7200:
            status = "{0} h".format(round(timeleft/3600, 1))
        if timeleft > 172800:
            status = "{0} d".format(round(timeleft/86400, 1))
    if isinstance(progress, int):
        progress = float(progress)
    if not isinstance(progress, float):
        progress = 0
        status = "error: progress var must be float\r\n"
    if progress < 0:
        progress = 0
        status = "Halt...\r\n"
    if progress >= 1:
        progress = 1
        status = "Done!\r\n"
    block = int(round(barLength*progress))
    text = "\rPercent: [{0}] {1}% {2}".format( "#"*block + "-"*(barLength-block), round(progress*100,1), status)
    sys.stdout.write("\033[K")
    sys.stdout.write(text)
    sys.stdout.flush()