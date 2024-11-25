from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class LeaderboardSerializer(serializers.ModelSerializer):
    reports_count = serializers.IntegerField()

    class Meta:
        model = User
        fields = ["id", "reports_count"]

    def to_representation(self, instance):
        rep = super().to_representation(instance)

        try:
            display_name = instance.oneid_profile.full_name
        except Exception as e:
            display_name = instance.username

        rep.update({
            "display_name": display_name
        })

        return rep
