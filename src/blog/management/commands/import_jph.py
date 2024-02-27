from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from jsonplaceholder.client import JSONPlaceholderClient
from blog.models import Post, Comment
from blog.serializers import JPHPostSerializer, JPHCommentSerializer


class Command(BaseCommand):

    MAX_BATCH_SIZE = 100

    help = """
    Imports data from JSON placeholder API. 
    
    Only posts and comments will be imported.
    """

    def handle(self, *args, **options):
        if Post.objects.count() or Comment.objects.count():
            raise CommandError('Database fact tables not empty, refusing import')
        
        client = JSONPlaceholderClient()

        with transaction.atomic():
            
            serializer = JPHPostSerializer(data=client.get_all("post"), many=True)
            serializer.is_valid(raise_exception=True)
            posts = [Post(**item) for item in serializer.validated_data]

            Post.objects.bulk_create(posts, batch_size=self.MAX_BATCH_SIZE)
            
            serializer = JPHCommentSerializer(data=client.get_all("comment"), many=True)
            serializer.is_valid(raise_exception=True)
            comments = [Comment(**item) for item in serializer.validated_data]

            Comment.objects.bulk_create(comments, batch_size=self.MAX_BATCH_SIZE)
