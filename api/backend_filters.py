from rest_framework.filters import BaseFilterBackend

class ClassicBackendFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        if view.action == "list":
            d = {}
            for key, value in request.query_params.items():
                if str(request.query_params.get(key)) == "":
                    d[key] = None
                else:
                    d[key] = request.query_params.get(key)
            queryset = queryset.filter(**d)
        return queryset

class OnlyUserFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        try:
            if request.is_admin:
                return queryset
            return queryset.filter(created_by=request.user)
        except Exception as ex:
            print(ex)
            return queryset