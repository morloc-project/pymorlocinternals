import json

"""
("tuple", [("float", None), ("record", OrderedDict(a=("float", None)))])
"""

def pack_list(x, schema):
  f = dispatch[schema[0]]
  return "[{}]".format(",".join([f(y, schema[1]) for y in x]))

def pack_tuple(x, schema):
  elements = []
  for (t, e) in zip(schema, x):
    f = dispatch[t[0]]
    elements.append(f(e, t[1]))
  return "[{}]".format(",".join(elements))

def pack_record(x, schema):
  entries = []
  for (k,t) in schema.items():
    f = dispatch[t[0]] 
    entries.append("{}={}".format(k, f(x[k], t[1])))
  return "{{{}}}".format(",".join(entries))

def pack_float(x, schema):
  return str(x)

def pack_int(x, schema):
  return str(x)

def pack_str(x, schema):
  return '"{}"'.format(x)

def pack_bool(x, schema):
  if x:
    return "true"
  else:
    return "false"

dispatch = dict(
    list = pack_list,
    tuple = pack_tuple,
    record = pack_record,
    float = pack_float,
    int = pack_int,
    str = pack_str,
    bool = pack_bool,
  )

def pack(x, schema):
  return (dispatch[schema[0]](x, schema[1]))

def unpack(x, t):
  return json.loads(x)
