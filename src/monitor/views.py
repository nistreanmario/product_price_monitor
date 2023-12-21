from django.db.models import OuterRef, Subquery
from django.db.models.functions import Coalesce
from django.utils import timezone
from django.views.generic import RedirectView
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Product, ProductsPrices
from .serializers import ProductSerializer, ProductResponseSerializer
from .services import CalculateAveragePriceService, ProductService


# Create your views here.
class RootRedirectView(RedirectView):
    pattern_name = 'schema-swagger-ui'
    permanent = False



class ProductsViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def list(self, request, *args, **kwargs):
        queryset = Product.objects.all()
        current_time = timezone.now()

        latest_price_subquery = ProductsPrices.objects.filter(
            product=OuterRef('pk')
        ).order_by('-created_at').values('price')[:1]

        current_price_subquery = ProductsPrices.objects.filter(
            product=OuterRef('pk'),
            start_date__lte=current_time,
            end_date__gte=current_time
        ).values('price')[:1]

        subquery = Coalesce(Subquery(current_price_subquery), Subquery(latest_price_subquery))

        serialized_data = queryset.annotate(
            price=subquery
        ).values('id', 'name', 'price')

        return Response(serialized_data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = ProductResponseSerializer(instance)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=ProductSerializer)
    def create(self, request, *args, **kwargs):
        try:
            serializer = ProductSerializer(data=request.data, context={'request': request})
            serializer.is_valid(raise_exception=True)

            product = ProductService.create_product_with_price(
                name=serializer.validated_data['name'],
                price=serializer.validated_data.get('price'),
                start_date=serializer.validated_data.get('start_date'),
                end_date=serializer.validated_data.get('end_date'),
            )
            response_serializer = ProductResponseSerializer(product)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        request_body=ProductSerializer,
        operation_description="If your start_date & end_date will match any existing product's price date range, "
                              "it will change its price value. In case if any of start_date or end_date overlaps with "
                              "any product's existing price date range, it will raise an error, if no will create a new price range "
    )
    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = ProductSerializer(instance, data=request.data)
            serializer.is_valid(raise_exception=True)

            price = serializer.validated_data.get('price')
            start_date = serializer.validated_data.get('start_date')
            end_date = serializer.validated_data.get('end_date')

            ProductService.update_product_with_price(
                instance=instance,
                price=price,
                start_date=start_date,
                end_date=end_date,
            )

            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)



class CalculateAveragePriceView(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('product_id', openapi.IN_PATH, type=openapi.TYPE_INTEGER),
            openapi.Parameter('start_date', openapi.IN_QUERY, type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE),
            openapi.Parameter('end_date', openapi.IN_QUERY, type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE),
        ],
    )
    def get(self, request, product_id, *args, **kwargs):
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        try:
            average_price = CalculateAveragePriceService.calculate_average_price(product_id, start_date, end_date)
            return Response({'average_price': average_price}, status=status.HTTP_200_OK)

        except NotFound as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)