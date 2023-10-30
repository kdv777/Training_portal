from rest_framework import serializers

from mainapp.models import Comment, Order, RatingStar


class OrderSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="course.name", read_only=True)

    class Meta:
        model = Order
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source="author.username", read_only=True)
    author_avatar = serializers.CharField(source="author.avatar", read_only=True)

    def get_fields(self):
        fields = super(CommentSerializer, self).get_fields()
        fields["children"] = CommentSerializer(many=True, read_only=True)
        return fields

    class Meta:
        model = Comment
        fields = "__all__"


class RatingStarSerializer(serializers.ModelSerializer):
    class Meta:
        model = RatingStar
        fields = "__all__"
