from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from api.paginations import CustomPaginator
from api.views import IsAuthenticated
from .models import Subscription, User
from .serializers import SubSerializer


class UserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer = SubSerializer
    pagination_class = CustomPaginator

    @action(
        detail=False,
        methods=['GET'],
        permission_classes=(IsAuthenticated,)
    )
    def subscriptions(self, request):
        user = self.request.user
        queryset = Subscription.objects.filter(sub=user)
        pages = self.paginate_queryset(queryset)
        serializer = SubSerializer(
            pages,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=(IsAuthenticated,)
    )
    def subscribe(self, request, id):
        user = request.user
        author = get_object_or_404(User, id=id)
        if self.request.method == 'POST':
            sub = Subscription.objects.create(sub=user,
                                              author=author)
            serializer = SubSerializer(sub)
            return Response(serializer.data)
        if self.request.method == 'DELETE':
            follow = get_object_or_404(Subscription, sub=user,
                                       author=author)
            follow.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
