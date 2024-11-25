from django.contrib.auth import get_user_model
from django.db.models import Count
from rest_framework import generics, response

from config.custom_paginations import CustomPagination
from petrol_spy.serializers import LeaderboardSerializer

User = get_user_model()


class GetLeaderboardView(generics.GenericAPIView):
    serializer_class = LeaderboardSerializer
    queryset = User.objects.all()
    pagination_class = CustomPagination

    def get_queryset(self):
        users = self.queryset.annotate(reports_count=Count('reports')).order_by("-reports_count")
        return users

    # @cache_page(60 * 1)
    def get(self, request, *args, **kwargs):
        paginator = self.pagination_class()
        paginated_obj = paginator.paginate_queryset(self.get_queryset(), request, view=self)
        serializer_data = self.serializer_class(paginated_obj, many=True).data

        return paginator.get_paginated_response(data=serializer_data)

    # def get_queryset(self):
    #     return self.queryset.annotate(
    #         reports_count=Count('user', distinct=True)
    #     ).order_by(
    #         "user", "reports_count"
    #     )[:100]
