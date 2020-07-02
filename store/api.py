from rest_framework import permissions, generics

from . models import Delivery
from . serializers import DeliverySerializer
from . permissions import CustomDjangoModelPermissions

class DeliveryListAPIView(generics.ListAPIView):
    """
    Model viewset for Deliveries
    """
    queryset = Delivery.objects.all()
    serializer_class = DeliverySerializer

class DeliveryListCreateAPIView(generics.ListCreateAPIView):
    """
    Model viewset for Create Delivery
    """
    queryset = Delivery.objects.all()
    serializer_class = DeliverySerializer
    permission_classes = [CustomDjangoModelPermissions]

    def get_queryset(self):
        return Delivery.objects.all()

class DeliveryRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Model viewset for Read/Update/Destroy Delivery
    """
    queryset = Delivery.objects.all()
    serializer_class = DeliverySerializer
    permission_classes = [CustomDjangoModelPermissions]