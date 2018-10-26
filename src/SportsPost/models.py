import re
from django.conf import settings
from django.urls import reverse
from django.db import models
from django.db.models.signals import post_save
from django.utils import timezone
from hashtags.signals import parsed_hashtags
# Create your models here.
class QuestionManager(models.Manager):
	def reshare(self, user, parent_obj):
		if parent_obj.parent:
			og_parent = parent_obj.parent
		else:
			og_parent = parent_obj
		qs = self.get_queryset().filter(user=user, parent=og_parent).filter(
				timestamp__year=timezone.now().year,
				timestamp__month=timezone.now().month,
				timestamp__day=timezone.now().day,
				reply=False,
			)
		if qs.exists():
			return None

		obj = self.model(
				parent  = og_parent,
				user    = user,
				content = parent_obj.content,
			)
		obj.save()
		return obj

	def like_toggle(self, user, sports_obj):
		if user in sports_obj.liked.all():
			is_liked = False
			sports_obj.liked.remove(user)
		else:
			is_liked = True
			sports_obj.liked.add(user)
		return is_liked
		
class Question(models.Model):
	parent      = models.ForeignKey("self", on_delete=models.CASCADE, blank=True, null=True)
	user 		= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	liked       = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='liked')
	reply       = models.BooleanField(verbose_name="Is a reply?", default=False)
	content 	= models.CharField(max_length=200)
	updated		= models.DateTimeField(auto_now=True)
	timestamp	= models.DateTimeField(auto_now_add=True)

	objects     = QuestionManager()

	def __str__(self):
		return str(self.content)

	def get_absolute_url(self):
		return reverse("postsports:detail", kwargs={"pk":self.pk})

	class Meta:
		ordering = ['-timestamp']

	def get_parent(self):
		the_parent = self 
		if self.parent:
			the_parent = self.parent
		return the_parent

	def get_children(self):
		parent = self.get_parent()
		qs = Question.objects.filter(parent=parent)
		qs_parent = Question.objects.filter(pk=parent.pk)
		return (qs | qs_parent)

def question_save_receiver(sender, instance, created, *args, **kwargs):
	if created and not instance.parent:
		hash_regex = r'#(?P<username>[\w\d-]+)'
		hashtags   = re.findall(hash_regex, instance.content)
		parsed_hashtags.send(sender=instance.__class__, hashtag_list=hashtags)

post_save.connect(question_save_receiver, sender=Question)