from rest_framework import mixins, viewsets


class ListViewSet(
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    """ViewSet исключительно для отображения."""

    pass
