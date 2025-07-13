import requests
import threading
from queue import Queue
from time import time

class FlaskAPITester:
    def __init__(self, base_url):
        """Inicializa el tester con la URL base de la API Flask"""
        self.base_url = base_url.rstrip('/')
        self.test_queue = Queue()
        self.results = []
    
    def add_test(self, endpoint, method='GET', data=None, expected_status=200):
        """Añade una prueba a la cola"""
        self.test_queue.put({
            'endpoint': endpoint,
            'method': method.upper(),
            'data': data,
            'expected': expected_status
        })
    
    def _worker(self):
        """Hilo worker que ejecuta las pruebas"""
        while not self.test_queue.empty():
            test = self.test_queue.get()
            url = f"{self.base_url}{test['endpoint']}"
            
            try:
                start_time = time()
                response = requests.request(
                    method=test['method'],
                    url=url,
                    json=test['data'],
                    timeout=5
                )
                elapsed = time() - start_time
                
                result = {
                    'url': url,
                    'method': test['method'],
                    'status': response.status_code,
                    'expected': test['expected'],
                    'time': round(elapsed, 3),
                    'success': response.status_code == test['expected'],
                    'response': response.json() if response.content else None
                }
                
            except Exception as e:
                result = {
                    'url': url,
                    'error': str(e),
                    'success': False
                }
            
            self.results.append(result)
            self.test_queue.task_done()
    
    def run_tests(self, workers=3):
        """Ejecuta todas las pruebas con workers concurrentes"""
        threads = []
        for _ in range(workers):
            t = threading.Thread(target=self._worker)
            t.start()
            threads.append(t)
        
        self.test_queue.join()
        
        for t in threads:
            t.join()
        
        return self.results

if __name__ == '__main__':
    # Ejemplo de uso
    tester = FlaskAPITester('http://localhost:5000')
    
    # Pruebas para la API Flask
    tester.add_test('/', 'GET', expected_status=200)
    tester.add_test('/users', 'GET', expected_status=200)
    tester.add_test('/users/1', 'GET', expected_status=200)
    tester.add_test('/users/99', 'GET', expected_status=404)
    tester.add_test('/users', 'POST', {'name': 'Charlie'}, expected_status=201)
    
    print("Ejecutando pruebas...")
    results = tester.run_tests()
    
    print("\nResultados:")
    for i, test in enumerate(results, 1):
        # Manejo seguro de las claves del diccionario
        method = test.get('method', 'N/A')
        url = test.get('url', 'URL no disponible')
        status = test.get('status', 'N/A')
        expected = test.get('expected', 'N/A')
        elapsed = test.get('time', 0)
        
        print(f"{i}. {method} {url} - ", end='')
        
        if test.get('success', False):
            print(f"✅ Éxito (Status: {status}, Tiempo: {elapsed:.3f}s)")
        else:
            print(f"❌ Fallo (Esperado: {expected}, Obtenido: {status})")
            if 'error' in test:
                print(f"   Error: {test['error']}")
            if 'response' in test and test['response']:
                print(f"   Respuesta: {test['response']}")