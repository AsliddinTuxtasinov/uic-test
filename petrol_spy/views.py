from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.db.models import Count
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import generics

from config.custom_paginations import CustomPagination
from petrol_spy.serializers import LeaderboardSerializer

User = get_user_model()


class GetLeaderboardView(generics.GenericAPIView):
    serializer_class = LeaderboardSerializer
    queryset = User.objects.all()
    pagination_class = CustomPagination

    def get_queryset(self):
        cache_key = "leaderboard_users"
        users = cache.get(cache_key)
        if not users:
            # Annotate with the count of reports and filter out users with 0 reports
            users = (
                self.queryset.annotate(reports_count=Count("reports"))
                .filter(reports_count__gt=0)  # Exclude reports_count = 0
                .order_by("-reports_count")[:100]
            )
            cache.set(cache_key, users, 60 * 3)  # Cache for 3 minutes

        return users

    @method_decorator(cache_page(60 * 3))
    def get(self, request, *args, **kwargs):
        paginator = self.pagination_class()
        paginated_obj = paginator.paginate_queryset(queryset=self.get_queryset(), request=request, view=self)
        serializer_data = self.serializer_class(paginated_obj, many=True).data

        return paginator.get_paginated_response(data=serializer_data)

    # def get_queryset(self):
    #     return self.queryset.annotate(
    #         reports_count=Count('user', distinct=True)
    #     ).order_by(
    #         "user", "reports_count"
    #     )[:100]
