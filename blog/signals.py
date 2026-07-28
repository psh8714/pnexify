from django.db.models import signals
from django.dispatch import receiver
from .models import Post, ImagePost, User


@receiver(signals.m2m_changed, sender=Post.likes.through)
def count_likes(sender, instance, **kwargs):
    instance.total_likes = instance.likes.count()
    instance.save()

@receiver(signals.post_delete, sender=ImagePost)
def delete_image_file(sender, instance, **kwargs):
    if instance.image_file:
        instance.image_file.delete(save=False)

# @receiver(signals.m2m_changed, sender=User.saved_posts.through)
# def count_saved_posts(sender, instance, **kwargs):
#     post = Post.objects.get(author=instance)
#     post.total_saves = instance.saved_posts.count()
#     post.save()