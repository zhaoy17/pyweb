from ..http import httpRequest


class Router:
    def __init__(self, root_object):
        self.root_object = root_object
        self.has_arg = None

    def _find_object(self, object_location):
        curr = self.root_object
        for i in range(len(object_location)):
            if i < len(object_location) - 1:
                try:
                    curr = getattr(curr, object_location[i])
                except AttributeError:
                    raise ValueError("Resource cannot be located")
            else:
                try:
                    curr = getattr(curr, object_location[i])
                    if not hasattr(curr, "__call__"):
                        raise ValueError("Resource cannot be located")
                    self.has_arg = False
                    return curr
                except AttributeError:
                    self.has_arg = True
                    return curr

    def execute_request(self, request: httpRequest) -> dict:
        target = self._find_object(request.object_location)
        if self.has_arg is not None:
            func = getattr(target, "do_" + request.method.lower())
            return func(request.object_location[-1], request.query_string)
        else:
            return target()
