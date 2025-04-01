class UserRegisterSerializer(serializers.ModelSerializer):
password = serializers.CharField(write_only=True, min_length=6)
class Meta:
model = User
fields = ['id', 'username', 'email', 'password']
def create(self, validated_data):
user = User.objects.create_user(**validated_data)
return user
class AdminRegisterSerializer(serializers.ModelSerializer):
password = serializers.CharField(write_only=True, min_length=6)
class Meta:
model = User
fields = ['id', 'username', 'email', 'password']
def create(self, validated_data):
user = User.objects.create_user(**validated_data)
user.is_staff = True
user.save()
return user
class UserLoginSerializer(serializers.Serializer):
username = serializers.CharField()
password = serializers.CharField(write_only=True)
class UserProfileSerializer(serializers.ModelSerializer):
class Meta:
model = UserProfile
fields = ['balance']
class UserSerializer(serializers.ModelSerializer):
is_admin = serializers.BooleanField(source='is_staff', read_only=True)
balance = serializers.DecimalField(
source='profile.balance',
max_digits=10,
decimal_places=2,
read_only=True,
default=0.00,
allow_null=True
)
class Meta:
model = User
fields = ['id', 'username', 'email', 'is_admin', 'balance']
class TransactionSerializer(serializers.ModelSerializer):
username = serializers.CharField(source='user.username', read_only=True)
class Meta:
model = Transaction
fields = ['id', 'username', 'amount', 'transaction_type', 'description', 'timestamp']
read_only_fields = ['id', 'username', 'transaction_type', 'timestamp']
class DepositSerializer(serializers.Serializer):
amount = serializers.DecimalField(max_digits=10, decimal_places=2)
def validate_amount(self, value):
if value <= 0:
raise serializers.ValidationError("Amount must be positive")
return value
class ChangePasswordSerializer(serializers.Serializer):
old_password = serializers.CharField(required=True)
new_password = serializers.CharField(required=True, validators=[validate_password])
confirm_password = serializers.CharField(required=True)
def validate(self, attrs):
if attrs['new_password'] != attrs['confirm_password']:
raise serializers.ValidationError({"confirm_password": "New passwords don't match."})
return attrs
class LogoutSerializer(serializers.Serializer):
refresh = serializers.CharField(required=True)
default_error_messages = {
'bad_token': 'Token is invalid or expired',
'blacklisted': 'Token has already been blacklisted'
}
def validate(self, attrs):
self.token = attrs['refresh']
return attrs
def save(self, **kwargs):
try:
RefreshToken(self.token).blacklist()
except TokenError:
self.fail('bad_token')