from rest_framework import serializers
# from datetime import datetime

from accounts.models import User

class UserSerializer(serializers.ModelSerializer):
    last_login  = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = [
            'id','email','username', 'first_name',
            'last_name','phone_number', 'is_active',
            'house_add','last_login',
        ]

    def get_last_login(self, obj):
        return obj.last_login.strftime("%d-%b-%Y")


class UpdateProfileSerializer(UserSerializer):

    email       = serializers.SerializerMethodField(read_only=True)
    username    = serializers.SerializerMethodField(read_only=True)

    def get_email(self, obj):
        return obj.email

    def get_username(self, obj):
        return obj.username


class UserRegisterSerializer(serializers.ModelSerializer):

    password            = serializers.CharField(style={'input_type':'password'}, write_only=True)
    confirm_password    = serializers.CharField(style={'input_type':'password'}, write_only=True)
    registration_id     = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'email',
            'username',
            'password',
            'confirm_password',
            'registration_id',
        ]
        extra_kwargs = {'password':{'write_only':True}, 'confirm_password':{'write_only':True}}

    def validate_password(self, value):
        """
        Validates that the password is at least 6 characters long
        """
        if len(value) < 6:
            raise serializers.ValidationError("Password must be at least six characters long")
        return value


    def validate(self, data):
        """
        Validates that the passwords are the same
        """
        pw              = data.get('password')
        pw2             = data.get('confirm_password')

        if pw != pw2:
            raise serializers.ValidationError("Passwords Must match")
        return data

    def create(self, validated_data):
        user_obj = User(
            username=validated_data.get('username'),
            email=validated_data.get('email')
        )
        user_obj.set_password(validated_data.get('password'))
        user_obj.save()

        # Work on returning Matric Number
        return user_obj