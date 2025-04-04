class OrderItemSerializer(serializers.ModelSerializer):
product_details = ProductSerializer(source='product', read_only=True)
class Meta:
model = OrderItem
fields = ['id', 'product', 'product_details', 'quantity', 'price']
extra_kwargs = {
'product': {'write_only': True}
}
class OrderSerializer(serializers.ModelSerializer):
items = OrderItemSerializer(many=True, read_only=True)
class Meta:
model = Order
fields = [
'id', 'user', 'full_name', 'address', 'phone',
'email', 'status', 'total_amount', 'items',
'created_at', 'updated_at'
]
read_only_fields = ['user', 'created_at', 'updated_at', 'total_amount']
class OrderCreateSerializer(serializers.ModelSerializer):
class Meta:
model = Order
fields = [
'full_name', 'address', 'phone',
'email'
]
def create(self, validated_data):
user = self.context['request'].user
validated_data['user'] = user
order = Order.objects.create(**validated_data)
return order