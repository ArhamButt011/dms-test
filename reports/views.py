from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import WageRate, WageRateDetail
from .serializers import WageRateSerializer, WageRateDetailSerializer
from rest_framework.decorators import api_view

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def create_wagerate(request, id=None):
    if request.method == 'GET':  # Corrected 'Get' to 'GET'
        if id:
            try:
                wage = WageRate.objects.get(pk=id)
                serializer = WageRateSerializer(wage)
            except WageRate.DoesNotExist:
                return Response({'message': 'The WageRate does not exist'}, status=status.HTTP_404_NOT_FOUND)
        else:
            wage = WageRate.objects.all()
            serializer = WageRateSerializer(wage, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = WageRateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'PUT' and id is not None:
        try:
            wage = WageRate.objects.get(pk=id)
        except WageRate.DoesNotExist:
            return Response({'message': 'The WageRate does not exist'}, status=status.HTTP_404_NOT_FOUND)

        serializer = WageRateSerializer(wage, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()

            update_nested_objects(request.data, wage)  # Ensure this function is correctly implemented
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE' and id is not None:
        try:
            wage = WageRate.objects.get(pk=id)
            wage.delete()
            return Response({'message': 'WageRate was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
        except WageRate.DoesNotExist:
            return Response({'message': 'The WageRate does not exist'}, status=status.HTTP_404_NOT_FOUND)

def update_nested_objects(data, wage_instance):
    detail_data = data.get('detail', [])
    for item_data in detail_data:
        item_id = item_data.pop('id', None)
        if item_id:
            WageRateDetail.objects.filter(id=item_id, title=wage_instance).update(**item_data)
        else:
            WageRateDetail.objects.create(title=wage_instance, **item_data)
