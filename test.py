import sys, os, os.path, json

sys.path.insert(0, os.path.join(os.path.split(__file__)[0], 'cson'))
import cson

total = 0
errors = []

def matches(name):
    return not sys.argv[1:] or name in sys.argv[1:]

srcdir = os.path.join(os.path.split(__file__)[0], 'test')
for name in os.listdir(srcdir):
    if not name.endswith('.cson'):
        continue
    if not matches(name):
        continue
    total += 1

    cson_fname = os.path.join(srcdir, name)
    with open(cson_fname, 'rb') as fin:
        try:
            c = cson.load(fin)
        except cson.ParseError as e:
            print('{}({},{}): error: {}'.format(name, e.line, e.col, e.msg))
            errors.append(name)
            continue

    json_name = name[:-5] + '.json'

    with open(os.path.join(srcdir, json_name), 'rb') as fin:
        j = json.loads(fin.read().decode('utf-8'))
    if c != j:
        print('error: {}'.format(name))
        print(repr(c))
        print(repr(j))
        errors.append(name)
        continue
    with open(os.path.join(srcdir, json_name), 'rb') as fin:
        try:
            c = cson.load(fin)
        except cson.ParseError as e:
            print('{}({},{}): error: {}'.format(json_name, e.line, e.col, e.msg))
            errors.append(name)
            continue
    if c != j:
        print('error: {}'.format(name))
        print(repr(c))
        print(repr(j))
        errors.append(name)

if errors:
    sys.exit(1)

print('succeeded: {}'.format(total))
