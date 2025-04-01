@api_view(['GET'])
def api_root(request, format=None):
return Response({
'users': {
'register': reverse('register', request=request, format=format),
'register_admin': reverse('register-admin', request=request, format=format),
'login': reverse('login', request=request, format=format),
'profile': reverse('profile', request=request, format=format),
'logout': reverse('logout', request=request, format=format),
'change_password': reverse('change-password', request=request, format=format),
'delete_account': reverse('delete-account', request=request, format=format),
'deposit': reverse('deposit-funds', request=request, format=format),
'transactions': reverse('transaction-history', request=request, format=format),
},
'products': {
'categories': reverse('category_list', request=request, format=format),
'list': reverse('product_list', request=request, format=format),
'add': reverse('add_product', request=request, format=format),
},
'cart': {
'view': reverse('view-cart', request=request, format=format),
'add': reverse('add-to-cart', request=request, format=format),
},
'orders': {
'list': reverse('order-list', request=request, format=format),
'create': reverse('create-order', request=request, format=format),
},
'docs': reverse('schema-swagger', request=request, format=format),
})
schema_view = get_schema_view(
openapi.Info(
title='E-COMMERCE STORE API',
default_version='v1',
description='This is the API for E-COMMERCE application',
terms_of_service='https://www.google.com/policies/terms/',
contact=openapi.Contact(email='gorgolasha@gmail.com')
),
public=True,
permission_classes=(AllowAny,),
authentication_classes=(SessionAuthentication, TokenAuthentication),
)
urlpatterns = [
path('admin/', admin.site.urls),
path('', api_root, name='api-root'),
path('products/', include('products.urls')),
path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger'),
path('users/', include('users.urls')),
path('cart/', include('cart.urls')),
path('orders/', include('orders.urls')),
]
if settings.DEBUG:
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)