import logging

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from ai_helper.serializers import AiTextSerializer
from ai_helper.ai_client import AiClient


logger = logging.getLogger('__name__')


class AiTextRefactoring(APIView):
    def post(self, request):
        serializer = AiTextSerializer(data=request.data)
        if serializer.is_valid():
            text = serializer.data['text']
            refactored_text = self.refactor_text_by_ai(text)
            return Response({'text': refactored_text})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def refactor_text_by_ai(self, text: str) -> str:
        try:
            ai_client = AiClient()
            refactored_text = ai_client.get_beautiful_text(text)
        except Exception as e:
            logger.warning(e)
            refactored_text = text
        return refactored_text
