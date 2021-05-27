from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from core.models import Post, Comment
from core.tests.data import user_data, post_data, comment_data


class PostTestCase(TestCase):

    def setUp(self):
        user = User.objects.create_user(**user_data)
        post_data['author'] = user
        self.post = Post.objects.create(**post_data)

    def test_type(self):
        self.assertTrue(isinstance(self.post, Post))

    def test_str(self):
        self.assertEqual(self.post.__str__(), self.post.title)

    def test_get_absolute_url(self):
        url = reverse('post_detail', args=[str(self.post.id)])
        self.assertEqual(self.post.get_absolute_url(), url)

    def test_get_comment_count(self):
        self.assertEqual(self.post.get_comment_count(), 0)
        comment_data['post'] = self.post
        comment = Comment.objects.create(**comment_data)
        comment.approve()
        self.assertEqual(self.post.get_comment_count(), 1)

    def test_get_summary(self):
        self.assertEqual(self.post.get_summary(), f'{self.post.text[:255]}...')


class CommentTestCase(TestCase):

    def setUp(self):
        user = User.objects.create(**user_data)
        post_data['author'] = user
        post = Post.objects.create(**post_data)
        comment_data['post'] = post
        self.comment = Comment.objects.create(**comment_data)

    def test_type(self):
        self.assertTrue(isinstance(self.comment, Comment))

    def test_str(self):
        self.assertEqual(self.comment.__str__(), self.comment.text[:15])

    def test_approve(self):
        self.assertFalse(self.comment.approved)
        self.comment.approve()
        self.comment.refresh_from_db()
        self.assertTrue(self.comment.approved)
