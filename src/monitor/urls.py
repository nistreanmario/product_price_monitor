# urls.py
from django.urls import path, include
from .views import CalculateAveragePriceView, ProductsViewSet
from rest_framework import permissions
from rest_framework.routers import DefaultRouter
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Your API",
        default_version='v1',
        description="Your API description",
        terms_of_service="https://www.yourapp.com/terms/",
        contact=openapi.Contact(email="contact@yourapp.com"),
        license=openapi.License(name="Your License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

router = DefaultRouter()
router.register(r'products', ProductsViewSet, basename='products')

urlpatterns = [
    path('', include(router.urls)),
    path('products/<int:product_id>/average_price/', CalculateAveragePriceView.as_view(), name='calculate-average-price'),
]
