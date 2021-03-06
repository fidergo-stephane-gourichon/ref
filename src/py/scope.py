import re

_RE_SCOPE = re.compile(r"^(?P<provider>[a-z]+)(\.(?P<path>[a-z\.]+))?(\[(?P<conds>.*)\])?\.(?P<fields>[\{\}a-z,_*]+)$")
_RE_SCOPE_COND = re.compile(r"^(?P<k>[a-z0-9_]+)(?P<op>(<=|>=|!=|<|>|=))(?P<v>[^,]+)$")


def split(scopes):
    # XXX TODO
    return [scopes]


class ScopeCondition:
    def __init__(self, cond, var, value):
        self.cond = cond
        self.var = var
        self.value = value

    def __repr__(self):
        return f"<ScopeCondition {self.var} {self.cond} {self.value!r}>"


def parse(scope):
    # XXX implemet better parsing

    m = _RE_SCOPE.match(scope)

    if not m:
        return None

    m = m.groupdict()
    provider, path, conds, fields = m['provider'], m['path'], m['conds'], m['fields']

    if conds:
        conds2 = []
        for cond in conds.split(','):
            cond_m = _RE_SCOPE_COND.match(cond)

            if not cond_m:
                raise ValueError("malformed scope")

            cond_m = cond_m.groupdict()
            k, op, v = cond_m['k'], cond_m['op'], cond_m['v']

            cond = ScopeCondition(op, k, v)

            conds2.append(cond)

        conds = conds2

    if fields != '*':
        if fields[0] == '{' and fields[-1] == '}':
            fields = fields[1:-1].split(',')
        else:
            fields = [fields]

    return provider, path, conds, fields
