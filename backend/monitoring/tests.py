from django.test import TestCase

from monitoring.models import SystemComponent


class SystemComponentTests(TestCase):
    def test_create_component(self):
        c = SystemComponent.objects.create(name='svc', component_type='service')
        self.assertEqual(str(c), 'svc')
        self.assertTrue(c.is_active)
