class Cart(models.Model):
user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cart")
total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
def __str__(self):
return f"Cart of {self.user.username}"
def update_total(self):
total = Decimal('0.00')
cart_items = self.items.all()
for item in cart_items:
total += item.product.price * item.quantity
self.total_amount = total
self.save()
return total
class CartItem(models.Model):
cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
product = models.ForeignKey(Product, on_delete=models.CASCADE)
quantity = models.PositiveIntegerField(default=1)
def __str__(self):
return f"{self.quantity} x {self.product.name} in {self.cart.user.username}'s cart"
def save(self, *args, **kwargs):
super().save(*args, **kwargs)
self.cart.update_total()
def delete(self, *args, **kwargs):
cart = self.cart
super().delete(*args, **kwargs)
cart.update_total()