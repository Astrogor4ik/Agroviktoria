from django.test import TestCase
#from unittest import TestCase


class ProductTest(TestCase):

    def test_cart(self):
        response = self.client.get('/cart/')
        self.assertEqual(response.status_code, 200)
        #print(response.status_code)

    def test_store(self):
        response = self.client.get('/store/')
        self.assertEqual(response.status_code, 200)
        #print(response.status_code)

    def test_clean_seed(self):
        response = self.client.get('/clean_seed/')
        self.assertEqual(response.status_code, 200)

    def test_checkout(self):
        response = self.client.get('/checkout/')
        self.assertEqual(response.status_code, 200)

    def test_register(self):
        response = self.client.get('/register/')
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)

    def test_about(self):
        response = self.client.get('/about/')
        self.assertEqual(response.status_code, 200)




# if __name__ == '__main__':
#     main()