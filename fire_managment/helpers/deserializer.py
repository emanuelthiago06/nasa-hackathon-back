class Deserializer:
    def __init__(self, request, kwargs):

        self.request = request
        self.kwargs = kwargs

    def deserialize(self, model=None):
        params = self.request.data if self.request.data else self.kwargs
        if self.request.GET.dict:
            params.update(self.request.GET.dict())
        if not model:
            return params
        deserialized_params = model(**{key: value for key, value in params.items() if value is not None})
        return deserialized_params 