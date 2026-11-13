from datetime import date
from rest_framework.test import APITestCase
from .models import Vehiculo

class VehiculoApiTests(APITestCase):
    url = '/api/vehiculos/'
    valid = {'marca': 'Toyota', 'modelo': 'Corolla', 'anio': 2024, 'color': 'Blanco'}

    def test_ciclo_crud(self):
        response = self.client.post(self.url, self.valid)
        self.assertEqual(response.status_code, 201)
        pk = response.data['id']
        self.assertIn('created_at', response.data)
        self.assertIn('updated_at', response.data)
        detail = f'{self.url}{pk}/'
        self.assertEqual(self.client.get(self.url).data[0]['id'], pk)
        self.assertEqual(self.client.get(detail).data['marca'], 'Toyota')
        updated = {**self.valid, 'color': 'Azul'}
        response = self.client.put(detail, updated)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['color'], 'Azul')
        self.assertEqual(Vehiculo.objects.get(pk=pk).color, 'Azul')
        self.assertEqual(self.client.delete(detail).status_code, 204)
        self.assertEqual(self.client.get(detail).status_code, 404)

    def test_obligatorios_vacios_y_anios_invalidos(self):
        for payload in [{}, {**self.valid, 'marca': '  '},
                        {**self.valid, 'anio': 1885},
                        {**self.valid, 'anio': date.today().year + 2},
                        {**self.valid, 'anio': 'texto'}]:
            with self.subTest(payload=payload):
                self.assertEqual(self.client.post(self.url, payload).status_code, 400)
        self.assertEqual(Vehiculo.objects.count(), 0)

    def test_put_exige_campos_y_fechas_son_solo_lectura(self):
        created = self.client.post(self.url, {**self.valid, 'id': 999, 'created_at': '2000-01-01T00:00:00Z'})
        self.assertNotEqual(created.data['created_at'][:4], '2000')
        detail = f"{self.url}{created.data['id']}/"
        self.assertEqual(self.client.put(detail, {'color': 'Negro'}).status_code, 400)
        self.assertEqual(self.client.patch(detail, {'color': 'Negro'}).status_code, 200)

    def test_json_y_metodos(self):
        self.assertTrue(self.client.get(self.url)['Content-Type'].startswith('application/json'))
        self.assertEqual(self.client.delete(self.url).status_code, 405)
        self.assertEqual(self.client.get(self.url + '999999/').status_code, 404)
