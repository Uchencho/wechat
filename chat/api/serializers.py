from rest_framework import serializers

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