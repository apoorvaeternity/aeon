from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import serializers
from core.models import Profile, Objective


class UserRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def validate_email(self, email):
        """
        Check that the email of user is unique.
        """
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("A user with that email already exists.")
        return email

    def create(self, validated_data):
        user = User.objects.create_user(username=validated_data['username'],
                                        password=validated_data['password'],
                                        email=validated_data['email'])
        user.save()
        profile = Profile.objects.create(user=user)
        profile.save()
        return profile


class UserAuthenticationSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                if not user.is_active:
                    msg = 'User account is disabled.'
                    raise serializers.ValidationError(msg, code='authorization')

            else:
                msg = 'Unable to log in with provided credentials.'
                raise serializers.ValidationError(msg, code='authorization')

        else:
            msg = 'Must include "username" and "password".'
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        attrs['token'] = Profile.objects._create_auth_token(user=user)
        return attrs


class UserLogoutSerializer(serializers.Serializer):
    def validate(self, attrs):
        user = self.context['request'].user
        if user.auth_token.key:
            Profile.objects._delete_auth_token(user)
        else:
            msg = 'User is not logged in.'
            raise serializers.ValidationError(msg, code='authorization')
        return attrs


class ObjectiveCreateSerializer(serializers.ModelSerializer):
    title = serializers.CharField(allow_null=False)
    target_date = serializers.DateField(allow_null=False)
    target_time = serializers.TimeField(allow_null=False)

    def save(self, **kwargs):
        Objective.objects.create(user=self.context['request'].user, title=self.validated_data['title'],
                                 target_time=self.validated_data['target_time'],
                                 target_date=self.validated_data['target_date'])

    class Meta:
        model = Objective
        fields = ('title', 'target_date', 'target_time')


class ObjectiveListSerializer(serializers.Serializer):
    title = serializers.SerializerMethodField()
    target_date = serializers.SerializerMethodField()
    target_time = serializers.SerializerMethodField()

    def get_target_date(self,obj):
        return obj.target_date
    def get_title(self,obj):
        return obj.title
    def get_target_time(self,obj):
        return obj.target_time



class MilestoneCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Objective
        fields = ('objective', 'title', 'target_date', 'target_time')
