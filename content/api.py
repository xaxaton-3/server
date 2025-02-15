from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from content.serializers import DefenderFormSerializer, DefenderFormDeleteSerializer
from content.models import Defender
from users.decorators import with_authorization


class PersonRequestCreate(APIView):
    serializer_class = DefenderFormSerializer

    def post(self, request):
        serializer = DefenderFormSerializer(data=request.data)
        if serializer.is_valid():
            new_request = serializer.save()
            return Response({'id': new_request.id})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class PersonRequestDelete(APIView):
    serializer_class = DefenderFormDeleteSerializer

    @with_authorization
    def post(self, request):
        defender_id = -1
        if request.user and request.user.is_superuser:
            defender_id = int(request.data.get('defender_id', -1))
            Defender.objects.filter(id=defender_id).delete()
            return Response({'id': defender_id})
        return Response({'id': defender_id}, status=status.HTTP_403_FORBIDDEN)

class PersonRequestsList(APIView):
    serializer_class = DefenderFormSerializer

    @with_authorization
    def get(self, request):
        if request.user and request.user.is_superuser:
            forms = [self.serializer_class(form).data for form in Defender.objects.filter(is_open=True)]
            return Response(forms)
        return Response({}, status=status.HTTP_403_FORBIDDEN)
