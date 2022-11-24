import sys
import logging

from django.apps import AppConfig


logger = logging.getLogger(__name__)

class PostsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'posts'


    def ready(self) -> None:
        is_manage_py = any(arg.casefold().endswith("manage.py") for arg in sys.argv)
        if is_manage_py:
            return

        from posts.models import Post
        logger.info("Creating 1m random posts...")
        for i in range(1000):
            logger.info(f"Creating batch {i} out of 1000")
            posts = [Post(title=f"Post {i}, {j}",content=f"Content {i}, {j}") for j in range(1000)]
            try:
                Post.objects.bulk_create(posts)
            except Exception as e:
                logger.error(str(e))
        logger.info(f"There are now {Post.objects.count()} posts in the database")
