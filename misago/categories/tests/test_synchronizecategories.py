from django.core.management import call_command
from django.test import TestCase
from django.utils.six import StringIO
from django.utils.six.moves import range

from misago.categories.management.commands import synchronizecategories
from misago.categories.models import Category
from misago.threads import testutils


class SynchronizeCategoriesTests(TestCase):
    def test_categories_sync(self):
        """command synchronizes categories"""
        category = Category.objects.all_categories()[:1][0]

        threads = [testutils.post_thread(category) for t in range(10)]
        for thread in threads:
            [testutils.reply_thread(thread) for r in range(5)]

        category.threads = 0
        category.posts = 0

        command = synchronizecategories.Command()

        out = StringIO()
        call_command(command, stdout=out)

        category = Category.objects.get(id=category.id)
        self.assertEqual(category.threads, 10)
        self.assertEqual(category.posts, 60)

        command_output = out.getvalue().splitlines()[-1].strip()
        self.assertEqual(command_output, 'Synchronized 3 categories')
