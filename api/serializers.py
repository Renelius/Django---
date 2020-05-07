from rest_framework import serializers
from bboard.models import Bd, Comment, Rubric


class RubricSerializer(serializers.ModelSerializer):
    class Meta:
        model=Rubric
        fields=('id','name')

class BdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bd
        fields= ('id', 'title', 'rubric', 'content', 'price', 'published')

class BdDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bd
        fields= ('id', 'title', 'rubric', 'content', 'price', 'published')


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields= ('bb', 'name', 'body', 'email')