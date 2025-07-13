import unittest
import app  # Importa tu aplicación Flask

class FlaskAPITestCase(unittest.TestCase):
    def setUp(self):
        """Configura el cliente de pruebas"""
        self.app = app.app.test_client()
        self.app.testing = True
    
    def test_home_endpoint(self):
        """Prueba el endpoint raíz"""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Bienvenido', response.data)
    
    def test_get_users(self):
        """Prueba obtener todos los usuarios"""
        response = self.app.get('/users')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(response.json, list))
    
    def test_create_user(self):
        """Prueba crear un nuevo usuario"""
        test_user = {'name': 'Test', 'role': 'tester'}
        response = self.app.post('/users', json=test_user)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], 'Test')

if __name__ == '__main__':
    unittest.main()