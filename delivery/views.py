from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import DeliveryZone, DeliveryCheck
from django.utils import timezone


@api_view(['GET'])
def check_delivery(request, pincode):
    """Check if delivery is available for a given pincode - Always available"""
    try:
        # Clean the pincode
        pincode = pincode.strip()
        
        # Always return delivery available for all pincodes
        return Response({
            'pincode': pincode,
            'is_deliverable': True,
            'delivery_charge': 0.00,
            'estimated_days': 3,
            'location': "All Areas",
            'message': "Delivery available to all areas"
        })
            
    except Exception as e:
        return Response({
            'error': 'Error checking delivery availability',
            'message': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def delivery_zones(request):
    """Get all available delivery zones"""
    zones = DeliveryZone.objects.filter(is_active=True).order_by('pincode')
    
    zone_data = []
    for zone in zones:
        zone_data.append({
            'pincode': zone.pincode,
            'city': zone.city,
            'state': zone.state,
            'country': zone.country,
            'delivery_charge': float(zone.delivery_charge),
            'estimated_days': zone.estimated_days,
            'is_deliverable': zone.is_deliverable
        })
    
    return Response(zone_data)
