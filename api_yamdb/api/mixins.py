from rest_framework import filters, mixins, viewsets

from api.permissions import AnonReadOnly, AuthorOrModeratorsOrReadOnly


class CreateListDestroyViewSet(mixins.CreateModelMixin,
                               mixins.ListModelMixin,
                               mixins.DestroyModelMixin,
                               viewsets.GenericViewSet):
    """
    Вьюсет, позволяющий осуществлять GET, POST и DELETE запросы.
    """

    permission_classes = (AnonReadOnly | AuthorOrModeratorsOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
