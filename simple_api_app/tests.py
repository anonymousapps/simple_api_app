from django.test import TestCase
from django.urls import reverse
from datetime import datetime

from .models import Status, Task

"""
Helper method to add a Status.
Returns the created object.
"""
def _add_status(name):
    return Status.objects.create(name=name)

"""
Helper method to add a Task.
Returns the created object.
"""
def _add_task(title, description, status, due_date):
    return Task.objects.create(
                        title=title, 
                        description=description, 
                        status=status,
                        due_date=due_date)

"""
Testing of the Index that displays the tasks
"""
class IndexViewTests(TestCase):

    def test_index_with_no_tasks(self):
        response = self.client.get(reverse('simple_api_app:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'simple_api_app/index.html')

    def test_index_with_a_task(self):
        status = _add_status('Active')
        _add_task('Title', 'Description', status, datetime(2025,12,28,12,55,59,0))

        response = self.client.get(reverse('simple_api_app:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'simple_api_app/index.html')

        self.assertContains(response, 'Title')
        self.assertContains(response, 'Description')
        self.assertContains(response, 'Active')

"""
Testing deleting tasks
"""
class TaskDeleteViewTests(TestCase):

    def test_the_confirmation_screen(self):
        status = _add_status('Active')
        task = _add_task('Title', 'Description', status, datetime(2025,12,28,12,55,59,0))
        
        response = self.client.get(reverse('simple_api_app:delete_task', kwargs={'pk': task.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'simple_api_app/delete_task.html')


    def test_deleting_a_task(self):
        # check we only delete one entry and it is the correct one!
        status = _add_status('Active')
        task_one = _add_task('Title 1', 'Description 1', status, datetime(2025,12,28,12,55,59,0))
        task_two = _add_task('Title 2', 'Description 2', status, datetime(2025,12,28,12,55,59,0))

        self.assertEqual(Task.objects.count(), 2)
        response = self.client.post(reverse('simple_api_app:delete_task', 
                                                kwargs={'pk': task_one.id}), follow=True)
        self.assertTemplateUsed(response, 'simple_api_app/index.html')
        self.assertEqual(response.status_code, 200)  
        self.assertEqual(Task.objects.count(), 1)
        self.assertQuerySetEqual(response.context['task_list'],[task_two])

    def test_deleting_a_task_but_cancelling(self):
        status = _add_status('Active')
        task = _add_task('Title 1', 'Description 1', status, datetime(2025,12,28,12,55,59,0))

        response = self.client.post(reverse('simple_api_app:delete_task', 
                                                kwargs={'pk': task.id}),
                                                data={'cancel': 'Cancel'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(response.context['task_list'],[task])

"""
Testing adding tasks
"""
class TaskAddTests(TestCase):

    def test_adding_a_task_screen(self):
        response = self.client.get(reverse('simple_api_app:add_task'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'simple_api_app/task.html')

    def test_adding_a_task(self):
        status = _add_status('Active')

        response = self.client.post(
                reverse('simple_api_app:add_task'),
                    data={
                    'title': 'Test Title', 
                    'description': 'Test Description',
                    'status': status.id, 
                    'due_date': datetime(2025,12,28,12,55,59,0)},
                    follow=True
        )

        self.assertEqual(Task.objects.count(), 1)
        self.assertContains(response, 'Test Title')
        self.assertContains(response, 'Test Description')

    def test_adding_a_task_but_cancelling(self):
        response = self.client.post(
                reverse('simple_api_app:add_task'),
                        data={'cancel': 'Cancel'}, # cancel the add
                        follow=True
        )
        self.assertEqual(Task.objects.count(), 0)
        self.assertContains(response, 'There are no tasks yet.')   

"""
Testing editing tasks
"""
class TaskEditTests(TestCase):

    def setUp(self):
        status = _add_status('Active')
        task = _add_task('Title 1', 'Description 1', status, datetime(2025,12,28,12,55,59,0))

    def test_editing_a_task_screen(self):
        task = Task.objects.first()

        response = self.client.get(reverse('simple_api_app:edit_task', args=(task.id,)))
        self.assertContains(response, 'Title 1')
        self.assertContains(response, 'Description 1')

    def test_editing_a_task(self):
        task = Task.objects.first()
        response = self.client.get(reverse('simple_api_app:edit_task',
                                            args=(task.id,)))
        form = response.context['form']
        data = form.initial
        data['title'] = 'New Title'

        response = self.client.post(reverse('simple_api_app:edit_task', 
                                    kwargs={'task_id': task.id}), 
                                    data, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Title 1')
        self.assertContains(response, 'New Title')

    def test_editing_a_task_but_cancelling(self):
        task = Task.objects.first()
        response = self.client.get(reverse('simple_api_app:edit_task',
                                            args=(task.id,)))
        form = response.context['form']
        data = form.initial
        data['title'] = 'New Title'
        data['cancel'] = 'Cancel' # cancel the edit

        response = self.client.post(reverse('simple_api_app:edit_task', 
                                    kwargs={'task_id': task.id}), 
                                    data, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Title 1')
        self.assertNotContains(response, 'New Title')