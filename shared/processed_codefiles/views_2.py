class IsAdminUser:
def __call__(self, request):
if not request.user.is_authenticated:
return False
return request.user.is_staff
class ProductPagination(PageNumberPagination):
page_size = 10
page_size_query_param = 'page_size'
max_page_size = 100
@swagger_auto_schema(
method='GET',
operation_summary='Get Category Details',
operation_description='This endpoint will return an Category Details',
responses={
status.HTTP_200_OK: CategorySerializer,
status.HTTP_400_BAD_REQUEST: openapi.Response(
description='Invalid Request',
)
}
)
@api_view(['GET'])
def category_list(request):
categories = Category.objects.all()
serializer = CategorySerializer(categories, many=True)
return Response(serializer.data, status=status.HTTP_200_OK)
@swagger_auto_schema(
method='GET',
operation_summary='Get Product list with Pagination & Filters',
operation_description='This endpoint returns a paginated list of products. '
'You can filter by category or price, search by name/description, and sort by price or date.',
manual_parameters=[
openapi.Parameter('search', openapi.IN_QUERY, description="Search by name or description", type=openapi.TYPE_STRING),
openapi.Parameter('category', openapi.IN_QUERY, description="Filter by category ID", type=openapi.TYPE_INTEGER),
openapi.Parameter('price', openapi.IN_QUERY, description="Filter by price", type=openapi.TYPE_NUMBER),
openapi.Parameter('ordering', openapi.IN_QUERY, description="Sort by price or date (e.g., 'price' or '-created_at')", type=openapi.TYPE_STRING),
openapi.Parameter('page', openapi.IN_QUERY, description="Page number for pagination", type=openapi.TYPE_INTEGER),
],
responses={200: ProductSerializer(many=True)}
)
@api_view(['GET'])
def product_list(request):
products = Product.objects.all()
category = request.GET.get('category')
if category:
products = products.filter(category__id=category)
price = request.GET.get('price')
if price:
products = products.filter(price=price)
search_query = request.GET.get('search')
if search_query:
products = products.filter(name__icontains=search_query) | products.filter(description__icontains=search_query)
ordering = request.GET.get('ordering', '-created_at')
products = products.order_by(ordering)
paginator = ProductPagination()
paginated_products = paginator.paginate_queryset(products, request)
serializer = ProductSerializer(paginated_products, many=True)
return paginator.get_paginated_response(serializer.data)
@swagger_auto_schema(
method='POST',
operation_summary='Create a New Product (Admin Only)',
operation_description='This endpoint allows admins to create a new product. Regular users do not have access.',
manual_parameters=[
openapi.Parameter(
'image',
openapi.IN_FORM,
type=openapi.TYPE_ARRAY,
items=openapi.Items(type=openapi.TYPE_FILE)
),
openapi.Parameter(
'category',
openapi.IN_FORM,
description=(
"Select a category by its ID. Available categories:\n"
+ "\n".join([f"- {c.id}: {c.name}" for c in Category.objects.all()])
),
type=openapi.TYPE_INTEGER,
enum=[c.id for c in Category.objects.all()]
)
],
request_body=ProductSerializer,
responses={
status.HTTP_201_CREATED: openapi.Response(
description='Product Created',
examples={'application/json': {'message': 'Product created successfully'}}
),
status.HTTP_403_FORBIDDEN: openapi.Response(
description='Not Authorized',
examples={'application/json': {'detail': 'You do not have permission to perform this action.'}}
),
status.HTTP_400_BAD_REQUEST: openapi.Response(
description='Invalid Request',
examples={'application/json': {"title": ["This field is required."]}}
)
}
)
@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
@permission_classes([IsAuthenticated])
def add_product(request):
if not request.user.is_staff:
return Response(
{"detail": "You do not have permission to perform this action."},
status=status.HTTP_403_FORBIDDEN
)
serializer = ProductSerializer(data=request.data)
if serializer.is_valid():
serializer.save()
return Response(serializer.data, status=status.HTTP_201_CREATED)
return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@swagger_auto_schema(
method='PUT',
operation_summary='Update Product Details (Admin Only)',
operation_description='This endpoint allows admins to update an existing product. Regular users do not have access.',
manual_parameters=[
openapi.Parameter(
'image',
openapi.IN_FORM,
type=openapi.TYPE_ARRAY,
items=openapi.Items(type=openapi.TYPE_FILE),
required=False
),
openapi.Parameter(
'category',
openapi.IN_FORM,
description=(
"Select a category by its ID. Available categories:\n"
+ "\n".join([f"- {c.id}: {c.name}" for c in Category.objects.all()])
),
type=openapi.TYPE_INTEGER,
enum=[c.id for c in Category.objects.all()],
required=False
)
],
request_body=ProductSerializer,
responses={
status.HTTP_200_OK: openapi.Response(
description='Product Updated',
examples={'application/json': {'message': 'Product updated successfully'}}
),
status.HTTP_403_FORBIDDEN: openapi.Response(
description='Not Authorized',
examples={'application/json': {'detail': 'You do not have permission to perform this action.'}}
),
status.HTTP_404_NOT_FOUND: openapi.Response(
description='Product Not Found',
examples={'application/json': {'detail': 'Product not found.'}}
),
status.HTTP_400_BAD_REQUEST: openapi.Response(
description='Invalid Request',
examples={'application/json': {"title": ["Invalid data provided."]}}
)
}
)
@api_view(['PUT'])
@parser_classes([MultiPartParser, FormParser])
@permission_classes([IsAuthenticated])
def update_product(request, product_id):
if not request.user.is_staff:
return Response(
{"detail": "You do not have permission to perform this action."},
status=status.HTTP_403_FORBIDDEN
)
product = get_object_or_404(Product, id=product_id)
serializer = ProductSerializer(product, data=request.data, partial=True)
if serializer.is_valid():
serializer.save()
return Response(serializer.data, status=status.HTTP_200_OK)
return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@swagger_auto_schema(
method='DELETE',
operation_summary='Delete Product (Admin Only)',
operation_description='This endpoint allows admins to delete an existing product. Regular users do not have access.',
responses={
status.HTTP_204_NO_CONTENT: openapi.Response(
description='Product Deleted',
examples={'application/json': {'message': 'Product deleted successfully'}}
),
status.HTTP_403_FORBIDDEN: openapi.Response(
description='Not Authorized',
examples={'application/json': {'detail': 'You do not have permission to perform this action.'}}
),
status.HTTP_404_NOT_FOUND: openapi.Response(
description='Product Not Found',
examples={'application/json': {'detail': 'Product not found.'}}
)
}
)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_product(request, product_id):
if not request.user.is_staff:
return Response(
{"detail": "You do not have permission to perform this action."},
status=status.HTTP_403_FORBIDDEN
)
product = get_object_or_404(Product, id=product_id)
product.delete()
return Response(status=status.HTTP_204_NO_CONTENT)