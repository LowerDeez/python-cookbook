from itertools import dropwhile


# For example, if you want to skip all of the initial comment lines, here’s one way to do it:

with open('/etc/passwd') as f:
    for line in dropwhile(lambda line: line.startswith('#'), f):
        print(line, end='')
        