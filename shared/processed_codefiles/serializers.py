class CartItemSerializer(serializers.ModelSerializer):
product = ProductSerializer(read_only=True)
product_id = serializers.PrimaryKeyRelatedField(
queryset=Product.objects.all(), source='product', write_only=True
)
class Meta:
model = CartItem
fields = ['id', 'product', 'product_id', 'quantity']
extra_kwargs = {
'quantity': {'default': 1}
}
class CartSerializer(serializers.ModelSerializer):
items = CartItemSerializer(many=True, read_only=True)
class Meta:
model = Cart
fields = ['id', 'user', 'items', 'total_amount']
read_only_fields = ['user', 'total_amount']