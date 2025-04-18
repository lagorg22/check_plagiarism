@swagger_auto_schema(
method='GET',
operation_summary='List user orders',
operation_description='Retrieves all orders made by the current user.',
responses={
200: OrderSerializer(many=True),
401: "Unauthorized - Authentication required"
}
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def order_list(request):
orders = Order.objects.filter(user=request.user).exclude(status='CANCELLED')
for order in orders:
if order.total_amount == 0:
order.recalculate_total()
serializer = OrderSerializer(orders, many=True)
return Response(serializer.data, status=status.HTTP_200_OK)
@swagger_auto_schema(
method='GET',
operation_summary='Get order details',
operation_description='Retrieves details of a specific order including all order items.',
manual_parameters=[
openapi.Parameter('order_id', openapi.IN_PATH, description="ID of the order", type=openapi.TYPE_INTEGER)
],
responses={
200: OrderSerializer,
404: "Not Found - Order not found",
401: "Unauthorized - Authentication required"
}
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def order_detail(request, order_id):
try:
order = Order.objects.get(id=order_id, user=request.user)
if order.status == 'CANCELLED':
return Response({"detail": "This order has been cancelled."}, status=status.HTTP_404_NOT_FOUND)
if order.total_amount == 0:
order.recalculate_total()
except Order.DoesNotExist:
return Response({"detail": "Order not found."}, status=status.HTTP_404_NOT_FOUND)
serializer = OrderSerializer(order)
return Response(serializer.data, status=status.HTTP_200_OK)
@swagger_auto_schema(
method='POST',
operation_summary='Create new order',
operation_description='Creates a new order from the current cart and clears the cart. Total amount is taken from the cart and deducted from user balance.',
request_body=OrderCreateSerializer,
responses={
201: OrderSerializer,
400: "Bad Request - Invalid data, empty cart, or insufficient balance",
401: "Unauthorized - Authentication required"
}
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_order(request):
user = request.user
if user.is_staff:
return Response(
{"detail": "Admin users cannot place orders."},
status=status.HTTP_400_BAD_REQUEST
)
try:
cart = Cart.objects.get(user=user)
cart_items = CartItem.objects.filter(cart=cart)
if not cart_items.exists():
return Response(
{"detail": "Your cart is empty. Please add items to your cart before placing an order."},
status=status.HTTP_400_BAD_REQUEST
)
except Cart.DoesNotExist:
return Response(
{"detail": "Your cart is empty. Please add items to your cart before placing an order."},
status=status.HTTP_400_BAD_REQUEST
)
if not hasattr(user, 'profile') or user.profile.balance is None or user.profile.balance < cart.total_amount:
return Response(
{"detail": f"Insufficient balance. Your balance: {user.profile.balance if hasattr(user, 'profile') and user.profile.balance is not None else '0.00'}, Order total: {cart.total_amount}"},
status=status.HTTP_400_BAD_REQUEST
)
serializer = OrderCreateSerializer(data=request.data, context={'request': request})
if serializer.is_valid():
with transaction.atomic():
order = serializer.save(total_amount=cart.total_amount)
for cart_item in cart_items:
if cart_item.quantity > cart_item.product.stock:
return Response({
"detail": f"Not enough stock for '{cart_item.product.name}'. Available: {cart_item.product.stock}"
}, status=status.HTTP_400_BAD_REQUEST)
OrderItem.objects.create(
order=order,
product=cart_item.product,
quantity=cart_item.quantity,
price=cart_item.product.price
)
cart_item.product.stock -= cart_item.quantity
cart_item.product.save()
order.recalculate_total()
if not user.profile.withdraw(order.total_amount):
raise Exception("Failed to withdraw funds from user balance")
cart_items.delete()
cart.total_amount = 0
cart.save()
order.refresh_from_db()
return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@swagger_auto_schema(
method='DELETE',
operation_summary='Cancel order',
operation_description='Cancels an order if it has not been shipped yet and refunds the amount to user balance.',
manual_parameters=[
openapi.Parameter('order_id', openapi.IN_PATH, description="ID of the order", type=openapi.TYPE_INTEGER)
],
responses={
200: openapi.Response(
description="Order cancelled successfully",
examples={'application/json': {'detail': 'Order cancelled successfully. Amount refunded: 50.00'}}
),
400: "Bad Request - Order cannot be cancelled",
404: "Not Found - Order not found",
401: "Unauthorized - Authentication required"
}
)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def cancel_order(request, order_id):
user = request.user
if user.is_staff:
return Response({"detail": "Admin users do not have orders to cancel."},
status=status.HTTP_400_BAD_REQUEST)
try:
order = Order.objects.get(id=order_id, user=user)
except Order.DoesNotExist:
return Response({"detail": "Order not found."}, status=status.HTTP_404_NOT_FOUND)
if order.status == 'CANCELLED':
return Response({"detail": "Order is already cancelled."},
status=status.HTTP_400_BAD_REQUEST)
if order.status in ['SHIPPED', 'DELIVERED']:
return Response({"detail": "Cannot cancel an order that has been shipped or delivered."},
status=status.HTTP_400_BAD_REQUEST)
with transaction.atomic():
order_items = OrderItem.objects.filter(order=order)
for item in order_items:
item.product.stock += item.quantity
item.product.save()
if order.total_amount == 0:
order.recalculate_total()
refund_amount = order.total_amount
refund_description = f"Refund for cancelled order #{order.id}"
if not user.profile.refund(refund_amount, refund_description):
return Response(
{"detail": "Failed to process refund."},
status=status.HTTP_400_BAD_REQUEST
)
order.status = 'CANCELLED'
order.save()
return Response(
{"detail": f"Order cancelled successfully. Amount refunded: {refund_amount}"},
status=status.HTTP_200_OK
)