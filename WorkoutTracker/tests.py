from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse
from WorkoutTracker.models import Exercise, Equipment, Muscle


# Create your tests here.


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='Fake user')

    def test_exercise_list_GET(self):
        self.client.force_login(user=self.user)
        response = self.client.get(reverse('exercise_list'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'exercise_list.html')

    def test_create_exercise_GET(self):
        self.client.force_login(user=self.user)
        response = self.client.get(reverse('create_exercise'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_exercise.html')

    def test_create_exercise_POST_add_new_exercise(self):
        self.client.force_login(user=self.user)
        fake_muscle = Muscle.objects.create(name='Fake muscle')
        fake_equipment_1 = Equipment.objects.create(name='Fake equipment 1')
        fake_equipment_2 = Equipment.objects.create(name='Fake equipment 2')
        response = self.client.post(reverse('create_exercise'), {
            'name': 'fake exercise',
            'description': 'fake description',
            'main_muscle_group': fake_muscle.id,
            'equipment_needed': [fake_equipment_1.id, fake_equipment_2.id]
        })

        self.assertEquals(response.status_code, 302)
        self.assertEquals(Exercise.objects.filter(name='fake exercise').count(), 1)

    def test_create_exercise_POST_add_new_exercise_without_equipment(self):
        self.client.force_login(user=self.user)
        fake_muscle = Muscle.objects.create(name='Fake muscle')
        response = self.client.post(reverse('create_exercise'), {
            'name': 'fake exercise',
            'description': 'fake description',
            'main_muscle_group': fake_muscle.id,
        })

        self.assertEquals(response.status_code, 302)
        self.assertEquals(Exercise.objects.filter(name='fake exercise').count(), 1)

    def test_delete_exercise_GET(self):
        self.client.force_login(user=self.user)
        fake_muscle = Muscle.objects.create(name='Fake muscle')
        fake_equipment_1 = Equipment.objects.create(name='Fake equipment 1')
        fake_equipment_2 = Equipment.objects.create(name='Fake equipment 2')
        fake_exercise = Exercise.objects.create(name='fake_exercise', main_muscle_group=fake_muscle, owner=self.user)
        fake_exercise.equipment_needed.add(fake_equipment_1, fake_equipment_2)
        response = self.client.get(reverse('delete_exercise', args=[fake_exercise.pk]))
        self.assertEquals(response.status_code, 302)
        self.assertEquals(Exercise.objects.count(), 0)






