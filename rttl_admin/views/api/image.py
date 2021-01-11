from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import ModelSerializer
from rttl_admin.models import Image
from logging import getLogger

logger = getLogger(__name__)


class ImageSerializer(ModelSerializer):
    def create(self, validated_data):
        repo = validated_data['repo']
        image, created = Image.objects.get_or_create(repo=repo, defaults={
            'tag': validated_data.get('tag'),
            'name': validated_data.get('name'),
            'description': validated_data.get('description')})
        return image

    class Meta:
        model = Image
        fields = '__all__'


class ImageView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = ImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        image_id = kwargs.get('image_id')
        if image_id:
            try:
                serializer = ImageSerializer(Image.objects.get(pk=image_id))
            except Image.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = ImageSerializer(Image.objects.all(), many=True)
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        image_id = kwargs['image_id']
        try:
            image = Image.objects.get(pk=image_id)
            image.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Image.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
