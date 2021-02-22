from rest_framework import serializers
from .models import Poll, Choice, Vote
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = '__all__'


class ChoiceSerializer(serializers.ModelSerializer):
    votes = VoteSerializer(many=True, required=False)

    class Meta:
        model = Choice
        fields = '__all__'


class PollSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, required=False)

    class Meta:
        model = Poll
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {
            "password": {
                'write_only': True
            }
        }

    def create(self, validated_data):
        email = validated_data.get("email")
        username = validated_data.get("username")

        user = User(username=username, email=email)
        user.set_password(validated_data.get("password"))

        user.save()
        t = Token(user=user)
        t.save()
        return user





