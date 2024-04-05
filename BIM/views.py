from django.shortcuts import render
from rest_framework.views import APIView
from .models import BIM
from .serializers import BimSerializer
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
# Create your views here.

class BIMViews(APIView):

    def get(self, request, id=None):
        if id:
            bim = get_object_or_404(BIM, id=id)
            serializer = BimSerializer(bim)
        else:
            bim = BIM.objects.all()
            serializer = BimSerializer(bim, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BimSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id=None):
        if not id:
            # If no id is provided, we cannot update an object. Return an error response.
            return Response({"error": "Method PUT requires an id."}, status=status.HTTP_400_BAD_REQUEST)
        
        bim = get_object_or_404(BIM, id=id)
        serializer = BimSerializer(bim, data=request.data, partial=True)  # Use partial=True for partial updates
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id=None):
        if not id:
            return Response({"error": "Method DELETE requires an id."}, status=status.HTTP_400_BAD_REQUEST)
        
        bim = get_object_or_404(BIM, id=id)
        bim.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)