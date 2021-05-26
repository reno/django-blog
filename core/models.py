from django.conf import settings
from django.db import models
from django.urls import reverse


class Post(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='Autor',
        on_delete=models.CASCADE
    )
    title = models.CharField('Título', max_length=200)
    text = models.TextField('Texto')
    created_at = models.DateTimeField('Data de publicação', auto_now_add=True)
    updated_at = models.DateTimeField('Última atualização', auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

    def get_comment_count(self):
        return Comment.objects.filter(post=self, approved=True).count()

    def get_summary(self):
        return f'{self.text[:255]}...'


class Comment(models.Model):
    post = models.ForeignKey(
        'core.Post',
        verbose_name='Postagem',
        related_name='comments',
        on_delete=models.CASCADE
    )
    author = models.CharField('Autor', max_length=200)
    text = models.TextField('Texto')
    created_at = models.DateTimeField('Data de publicação', auto_now_add=True)
    approved = models.BooleanField('Aprovado', default=False)

    def __str__(self):
        return self.text[:15]

    def approve(self):
        self.approved = True
        self.save()
