from rest_framework import routers
from shop import api_views as myapp_views

router = routers.DefaultRouter()
router.register(r'products', myapp_views.ProductViewset,
                basename='products-mvs')
router.register(r'orders', myapp_views.OrderViewset)
router.register(r'order-items', myapp_views.OrderItemViewset)
