
def jsonify(instance, allow=None, exclude=[]):
    modelcls = type(instance)
    if allow:
        fn = (lambda x: x.name in allow)
    else:
        fn = (lambda x: x.name not in exclude)
    return {k.name:getattr(instance, k.name) for k in filter(fn, modelcls._meta.fields)}

