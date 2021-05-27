from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

from core.models import Post, Comment
from .data import user_data, post_data, comment_data


class ViewTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(**user_data)
        post_data['author'] = self.user
        self.post = Post.objects.create(**post_data)
        comment_data['post'] = self.post
        self.comment = Comment.objects.create(**comment_data)

    def test_login(self):
        url = reverse('login')
        response = self.client.post(url, user_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.user.is_authenticated)

    def test_logout(self):
        self.client.login(**user_data)
        url = reverse('logout')
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)

    def test_post_list(self):
        url = reverse('post_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post.title)
        self.assertContains(response, self.post.get_summary())

    def test_post_detail(self):
        url = reverse('post_detail', args=[self.post.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post.title)
        self.assertContains(response, self.post.text)

    def test_create_post(self):
        count = Post.objects.count()
        self.client.login(**user_data)
        url = reverse('post_new')
        response = self.client.post(url, post_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Post.objects.count(), count+1)

    def test_update_post(self):
        count = Post.objects.count()
        self.client.login(**user_data)
        url = reverse('post_edit', args=[self.post.id])
        response = self.client.post(url, post_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Post.objects.count(), count)

    def test_delete_post(self):
        self.client.login(**user_data)
        url = reverse('post_remove', args=[self.post.id])
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Post.objects.count(), 0)

    def test_create_comment(self):
        count = Comment.objects.count()
        url = reverse('add_comment_to_post', args=[self.post.id])
        response = self.client.post(url, comment_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Comment.objects.count(), count+1)

    def test_comment_approve(self):
        self.client.login(**user_data)
        url = reverse('comment_approve', args=[self.comment.id])
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.comment.refresh_from_db()
        self.assertTrue(self.comment.approved)

    def test_comment_remove(self):
        self.client.login(**user_data)
        url = reverse('comment_remove', args=[self.comment.id])
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Comment.objects.count(), 0)
