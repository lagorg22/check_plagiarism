class UserProfile(models.Model):
user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
balance = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'), null=True, blank=True)
def __str__(self):
return f"{self.user.username}'s profile"
def save(self, *args, **kwargs):
if self.user.is_staff:
self.balance = None
super().save(*args, **kwargs)
def deposit(self, amount):
if self.user.is_staff:
return False
if amount <= 0:
return False
if self.balance is None:
self.balance = Decimal('0.00')
self.balance += Decimal(str(amount))
self.save()
Transaction.objects.create(
user=self.user,
amount=amount,
transaction_type='DEPOSIT',
description='Funds deposited'
)
return True
def withdraw(self, amount):
if self.user.is_staff:
return False
if amount <= 0:
return False
if self.balance is None or self.balance < amount:
return False
self.balance -= Decimal(str(amount))
self.save()
Transaction.objects.create(
user=self.user,
amount=-amount,  # Negative for withdrawals
transaction_type='WITHDRAWAL',
description='Order payment'
)
return True
def refund(self, amount, description='Order refund'):
if self.user.is_staff:
return False
if amount <= 0:
return False
if self.balance is None:
self.balance = Decimal('0.00')
self.balance += Decimal(str(amount))
self.save()
Transaction.objects.create(
user=self.user,
amount=amount,
transaction_type='REFUND',
description=description
)
return True
class Transaction(models.Model):
TRANSACTION_TYPES = [
('DEPOSIT', 'Deposit'),
('WITHDRAWAL', 'Withdrawal'),
('REFUND', 'Refund'),
]
user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
amount = models.DecimalField(max_digits=10, decimal_places=2)
transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
description = models.CharField(max_length=255, blank=True)
timestamp = models.DateTimeField(auto_now_add=True)
class Meta:
ordering = ['-timestamp']
def __str__(self):
return f"{self.transaction_type} - {self.amount} - {self.user.username}"
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
if created:
UserProfile.objects.create(user=instance)
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
if not hasattr(instance, 'profile'):
UserProfile.objects.create(user=instance)