from django.db import models
from django.contrib.auth.models import User
from django.dispatch import Signal
from .utilities import send_activation_notification
from django.conf import settings
from datetime import datetime
from os.path import splitext

def get_timestamp_path(instance, filename):
    return '%s%s' % (datetime.now().timestamp(), splitext(filename)[1])

class Bd(models.Model):
    title = models.CharField(max_length=50, verbose_name='Товар')
    content = models.TextField(null=True, blank=True,verbose_name='Описание')
    price = models.FloatField(null=True, blank=True, verbose_name='Цена')
    published = models.DateTimeField(auto_now_add = True, db_index = True,verbose_name='Опубликовано')
    rubric = models.ForeignKey('Rubric', null=True, on_delete=models.PROTECT, verbose_name='Рубрика')
    author = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='Владелец объявления',null=True)

    class Meta:
        verbose_name_plural = 'Объявления'
        verbose_name = 'Объявление'
        ordering = ['-published']

class Images(models.Model):
    objects = None
    bb = models.ForeignKey(Bd, related_name='Объявление', on_delete=models.CASCADE)
    img = models.ImageField(verbose_name='Изображение', upload_to='', null=True, blank=True)


class Rubric(models.Model):
    def __str__(self):
        return self.name
    name = models.CharField(max_length=20, db_index=True, verbose_name='Название')

    class Meta:
        verbose_name_plural='Рубрики'
        verbose_name='Рубрика'
        ordering=['name']

class Comment(models.Model):
    bb = models.ForeignKey(Bd, related_name='comments',on_delete=models.PROTECT)
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    class Meta:
        ordering = ('created',)

    def __str__(self):
        return 'Comment by {} on {}'.format(self.name, self.post)


#Signal add comment
def post_save_dispatcher(sender, **kwargs):
    print(kwargs['instance'].body)
comment_save=Signal(providing_args=['instance'])
comment_save.connect(post_save_dispatcher, sender=Comment)


#Signal send email
def user_registrated_dispatcher(sender, **kwargs):
    send_activation_notification(kwargs['instance'])
user_registrated = Signal(providing_args=['instance'])
user_registrated.connect(user_registrated_dispatcher)