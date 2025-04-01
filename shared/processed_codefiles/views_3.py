UserRegisterSerializer, UserLoginSerializer, UserSerializer,
LogoutSerializer, AdminRegisterSerializer, ChangePasswordSerializer,
DepositSerializer, TransactionSerializer
)
@swagger_auto_schema(
method='POST',
operation_summary='Register a New User',
operation_description='This endpoint allows a new user to register by providing a username, email, and password.',
request_body=UserRegisterSerializer,
responses={
status.HTTP_201_CREATED: openapi.Response(
description='User registered successfully',
examples={'application/json': {'message': 'User registered successfully'}}
),
status.HTTP_400_BAD_REQUEST: openapi.Response(
description='Invalid data provided',
examples={'application/json': {'username': ['This field is required.']}}
)
}
)
@api_view(['POST'])
def register_user(request):
serializer = UserRegisterSerializer(data=request.data)
if serializer.is_valid():
serializer.save()
return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@swagger_auto_schema(
method='POST',
operation_summary='User Login',
operation_description='This endpoint authenticates a user and returns JWT tokens (access and refresh).',
request_body=UserLoginSerializer,
responses={
status.HTTP_200_OK: openapi.Response(
description='Login successful',
examples={'application/json': {'access': 'access_token', 'refresh': 'refresh_token'}}
),
status.HTTP_401_UNAUTHORIZED: openapi.Response(
description='Invalid credentials',
examples={'application/json': {'error': 'Invalid credentials'}}
)
}
)
@api_view(['POST'])
def login_user(request):
serializer = UserLoginSerializer(data=request.data)
if serializer.is_valid():
username = serializer.validated_data['username']
password = serializer.validated_data['password']
user = authenticate(username=username, password=password)
if user:
refresh = RefreshToken.for_user(user)
return Response({
"access": str(refresh.access_token),
"refresh": str(refresh)
}, status=status.HTTP_200_OK)
return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@swagger_auto_schema(
method='GET',
operation_summary='Get User Profile',
operation_description='This endpoint returns the profile of the authenticated user, including balance for regular users.',
responses={
status.HTTP_200_OK: openapi.Response(
description='User profile retrieved successfully',
examples={'application/json': {'id': 1, 'username': 'testuser', 'email': 'test@example.com', 'is_admin': False, 'balance': '100.00'}}
),
status.HTTP_401_UNAUTHORIZED: openapi.Response(
description='Authentication credentials were not provided or are invalid.',
examples={'application/json': {'detail': 'Authentication credentials were not provided.'}}
)
}
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request):
serializer = UserSerializer(request.user)
return Response(serializer.data, status=status.HTTP_200_OK)
@swagger_auto_schema(
method='POST',
operation_summary='User Logout',
operation_description=,
request_body=openapi.Schema(
type=openapi.TYPE_OBJECT,
required=['refresh'],
properties={
'refresh': openapi.Schema(
type=openapi.TYPE_STRING,
description='The refresh token issued during login'
)
}
),
responses={
status.HTTP_205_RESET_CONTENT: openapi.Response(
description='Logged out successfully',
examples={'application/json': {'message': 'Logged out successfully'}}
),
status.HTTP_400_BAD_REQUEST: openapi.Response(
description='Invalid refresh token',
examples={'application/json': {'refresh': ['Invalid token']}}
),
status.HTTP_401_UNAUTHORIZED: openapi.Response(
description='Authentication required',
examples={'application/json': {'detail': 'Authentication credentials were not provided.'}}
)
}
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_user(request):
serializer = LogoutSerializer(data=request.data)
if serializer.is_valid():
try:
serializer.save()
return Response(
{"message": "Logged out successfully"},
status=status.HTTP_205_RESET_CONTENT
)
except Exception as e:
return Response(
{"detail": str(e)},
status=status.HTTP_400_BAD_REQUEST
)
return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@swagger_auto_schema(
method='POST',
operation_summary='Register an Admin User',
operation_description='This endpoint allows registering an admin user with special privileges. In a production environment, this would be secured.',
request_body=AdminRegisterSerializer,
responses={
status.HTTP_201_CREATED: openapi.Response(
description='Admin user registered successfully',
examples={'application/json': {'message': 'Admin user registered successfully'}}
),
status.HTTP_400_BAD_REQUEST: openapi.Response(
description='Invalid data provided',
examples={'application/json': {'username': ['This field is required.']}}
)
}
)
@api_view(['POST'])
def register_admin(request):
serializer = AdminRegisterSerializer(data=request.data)
if serializer.is_valid():
serializer.save()
return Response({"message": "Admin user registered successfully"}, status=status.HTTP_201_CREATED)
return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@swagger_auto_schema(
method='PUT',
operation_summary='Change User Password',
operation_description='This endpoint allows a user to change their password after verifying their old password.',
request_body=ChangePasswordSerializer,
responses={
status.HTTP_200_OK: openapi.Response(
description='Password changed successfully',
examples={'application/json': {'message': 'Password changed successfully'}}
),
status.HTTP_400_BAD_REQUEST: openapi.Response(
description='Invalid data provided',
examples={'application/json': {'old_password': ['Wrong password.']}}
),
status.HTTP_401_UNAUTHORIZED: openapi.Response(
description='Authentication required',
examples={'application/json': {'detail': 'Authentication credentials were not provided.'}}
)
}
)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def change_password(request):
user = request.user
serializer = ChangePasswordSerializer(data=request.data)
if serializer.is_valid():
if not user.check_password(serializer.validated_data['old_password']):
return Response(
{"old_password": ["Wrong password."]},
status=status.HTTP_400_BAD_REQUEST
)
user.set_password(serializer.validated_data['new_password'])
user.save()
return Response(
{"message": "Password changed successfully"},
status=status.HTTP_200_OK
)
return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@swagger_auto_schema(
method='DELETE',
operation_summary='Delete User Account',
operation_description='This endpoint allows a user to delete their own account.',
request_body=openapi.Schema(
type=openapi.TYPE_OBJECT,
required=['password'],
properties={
'password': openapi.Schema(
type=openapi.TYPE_STRING,
description='Current password to confirm account deletion'
)
}
),
responses={
status.HTTP_204_NO_CONTENT: openapi.Response(
description='Account deleted successfully'
),
status.HTTP_400_BAD_REQUEST: openapi.Response(
description='Invalid password',
examples={'application/json': {'password': ['Wrong password.']}}
),
status.HTTP_401_UNAUTHORIZED: openapi.Response(
description='Authentication required',
examples={'application/json': {'detail': 'Authentication credentials were not provided.'}}
)
}
)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_account(request):
user = request.user
password = request.data.get('password')
if not password:
return Response(
{"password": ["This field is required."]},
status=status.HTTP_400_BAD_REQUEST
)
if not user.check_password(password):
return Response(
{"password": ["Wrong password."]},
status=status.HTTP_400_BAD_REQUEST
)
user.delete()
return Response(status=status.HTTP_204_NO_CONTENT)
@swagger_auto_schema(
method='POST',
operation_summary='Deposit Funds',
operation_description='This endpoint allows a user to deposit funds to their balance. Admin users cannot deposit funds.',
request_body=DepositSerializer,
responses={
status.HTTP_200_OK: openapi.Response(
description='Funds deposited successfully',
examples={'application/json': {'message': 'Deposit successful', 'new_balance': '150.00'}}
),
status.HTTP_400_BAD_REQUEST: openapi.Response(
description='Invalid amount or admin user',
examples={'application/json': {'error': 'Amount must be positive'}}
),
status.HTTP_401_UNAUTHORIZED: openapi.Response(
description='Authentication required',
examples={'application/json': {'detail': 'Authentication credentials were not provided.'}}
)
}
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def deposit_funds(request):
if request.user.is_staff:
return Response(
{"error": "Admin users cannot have a balance"},
status=status.HTTP_400_BAD_REQUEST
)
serializer = DepositSerializer(data=request.data)
if serializer.is_valid():
amount = serializer.validated_data['amount']
with transaction.atomic():
deposit_successful = request.user.profile.deposit(amount)
if deposit_successful:
return Response({
"message": "Deposit successful",
"new_balance": request.user.profile.balance
}, status=status.HTTP_200_OK)
else:
return Response({
"error": "Deposit failed"
}, status=status.HTTP_400_BAD_REQUEST)
return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@swagger_auto_schema(
method='GET',
operation_summary='Get Transaction History',
operation_description='This endpoint returns the transaction history of the authenticated user.',
responses={
status.HTTP_200_OK: TransactionSerializer(many=True),
status.HTTP_401_UNAUTHORIZED: openapi.Response(
description='Authentication required',
examples={'application/json': {'detail': 'Authentication credentials were not provided.'}}
)
}
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def transaction_history(request):
transactions = Transaction.objects.filter(user=request.user)
serializer = TransactionSerializer(transactions, many=True)
return Response(serializer.data, status=status.HTTP_200_OK)