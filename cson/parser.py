from peg import peg

def load(fin):
    return loads(fin.read())

def loads(s):
    return peg(s, _p_root)

def _p_ws(p):
    p('[ \t]*')

def _p_nl(p):
    p(r'([ \t]*(?:#[^\n]*)?\r?\n)+')

def _p_ews(p):
    with p:
        p(_p_nl)
    p(_p_ws)

def _p_id(p):
    return p(r'[$a-zA-Z_][$0-9a-zA-Z_]*')

def _p_string(p):
    with p:
        return p(r'"""(?:\\.|(?!""")(?!#\{).)*"""')[3:-3]
    with p:
        return p(r"'''(?:\\.|(?!''')(?!#\{).)*'''")[3:-3]
    with p:
        return p(r'"(?!"")(?:\\.|(?!#\{)[^"])*"')[1:-1]
    return p(r"'(?!'')(?:\\.|(?!#\{)[^'])*'")[1:-1]

def _p_array_value(p):
    with p:
        p(_p_nl)
        return p(_p_object)
    with p:
        p(_p_ws)
        return p(_p_line_object)
    p(_p_ews)
    return p(_p_simple_value)

def _p_key(p):
    with p:
        return p(_p_id)
    return p(_p_string)

def _p_flow_kv(p):
    k = p(_p_key)
    p(_p_ews)
    p(':')
    with p:
        p(_p_nl)
        return k, p(_p_object)
    with p:
        p(_p_ws)
        return k, p(_p_line_object)
    p(_p_ews)
    return k, p(_p_simple_value)

def _p_simple_value(p):
    with p:
        p('null')
        return None

    with p:
        p('false')
        return False
    with p:
        p('true')
        return True

    with p:
        return int(p('0b[01]+')[2:], 2)
    with p:
        return int(p('0o[0-7]+')[2:], 8)
    with p:
        return int(p('0x[0-9a-fA-F]+')[2:], 16)
    with p:
        return float(p(r'-?(?:[1-9][0-9]*|0)?\.[0-9]+(?:e[\+-]?[0-9]+)?|(?:[1-9][0-9]*|0)(?:\.[0-9]+)e[\+-]?[0-9]+'))
    with p:
        return int(p('-?[1-9][0-9]*|0'), 10)

    with p:
        return p(_p_string)

    with p:
        p(r'\[')
        r = []
        with p:
            p.set('I', '')
            r.append(p(_p_array_value))
            with p:
                while True:
                    with p:
                        p(_p_ews)
                        p(',')
                        rr = p(_p_array_value)
                    if not p:
                        p(_p_nl)
                        with p:
                            rr = p(_p_object)
                        if not p:
                            p(_p_ews)
                            rr = p(_p_simple_value)
                    r.append(rr)
                    p.commit()
            with p:
                p(_p_ews)
                p(',')
        p(_p_ews)
        p(r'\]')
        return r

    p(r'\{')

    r = {}
    p(_p_ews)
    with p:
        p.set('I', '')
        k, v = p(_p_flow_kv)
        r[k] = v
        p(_p_ews)
        with p:
            while True:
                p(',')
                p(_p_ews)
                k, v = p(_p_flow_kv)
                r[k] = v
                p(_p_ews)
                p.commit()
        with p:
            p(',')
            p(_p_ews)
    p(r'\}')
    return r

def _p_line_kv(p):
    k = p(_p_key)
    p(_p_ws)
    p(':')
    p(_p_ws)
    with p:
        p(_p_nl)
        p(p.get('I'))
        return k, p(_p_indented_object)
    with p:
        return k, p(_p_line_object)
    with p:
        return k, p(_p_simple_value)
    p(_p_nl)
    p(p.get('I'))
    p('[ \t]')
    p(_p_ws)
    return k, p(_p_simple_value)

def _p_line_object(p):
    k, v = p(_p_line_kv)
    r = { k: v }
    with p:
        while True:
            p(_p_ws)
            p(',')
            p(_p_ws)
            k, v = p(_p_line_kv)
            r[k] = v # uniqueness
            p.commit()
    return r

def _p_object(p):
    p.set('I', p.get('I') + p('[ \t]*'))
    r = p(_p_line_object)
    with p:
        while True:
            p(_p_ws)
            with p:
                p(',')
            p(_p_nl)
            p(p.get('I'))
            rr = p(_p_line_object)
            r.update(rr) # unqueness
            p.commit()
    return r

def _p_indented_object(p):
    p.set('I', p.get('I') + p('[ \t]'))
    return p(_p_object)

def _p_root(p):
    with p:
        p(_p_nl)

    with p:
        p.set('I', '')
        r = p(_p_object)
        p(_p_ws)
        with p:
            p(',')

    if not p:
        p(_p_ws)
        r = p(_p_simple_value)

    p(_p_ews)
    p(p.eof)
    return r
