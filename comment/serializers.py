from rest_framework import serializers

from user.serializers import UserSerializer
from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = "__all__"

