from django.test import TestCase, Client

from .models import User, Pet, Insurance, Visit, Vaccination

# Create your tests here.

class PetclinicTestCase(TestCase):
    
    def setUp(self):
    
        # Create users.
        a1 = User.objects.create(id=1, username=123, identical_number=123, first_name="a", last_name="b", phone_number="010-1002030")
        a1.set_password('12345')
        a1.save()
        a2 = User.objects.create(id=2, username=987, identical_number=987, first_name="c", last_name="d", phone_number="010-2005070")
        a3 = User.objects.create(id=3, username=0, identical_number=0, first_name="e", last_name="f", phone_number="")
        a4 = User.objects.create(id=4, username=234, identical_number=234, first_name="e", last_name="", phone_number="010-2005080")

        # Create pets.
        pet1 = Pet.objects.create(id=1, icon="🐰", nickname="Ted", birth_date="2018-02-07", pet_type="cat", details="ragdoll", owner=a1)
        pet2 = Pet.objects.create(id=2, icon="🐶", nickname="Jojo", birth_date="2020-12-25", pet_type="dog", details="papillon", owner=a2)
        pet3 = Pet.objects.create(id=3, icon="🐩", nickname="", birth_date="2019-11-05", pet_type="dog", details="", owner=a2)

        # Create insurance.
        i1 = Insurance.objects.create(id=1, start_date="2023-12-01", monthly_price=25, owner=a1, pet=pet1)
        i2 = Insurance.objects.create(id=2, start_date="2023-11-29", monthly_price=30, owner=a2, pet=pet2)
        i3 = Insurance.objects.create(id=3, start_date="2023-11-28", monthly_price=0, owner=a2, pet=pet1)
    
        # Create visit.
        v1 = Visit.objects.create(id=1, date_visit="2023-11-29", time_visit="09:30", type_visit="Consulting", pet=pet1)
        v2 = Visit.objects.create(id=2, date_visit="2023-11-30", time_visit="16:00", type_visit="Vaccination", pet=pet2)
        v3 = Visit.objects.create(id=3, date_visit="2023-11-29", time_visit="", type_visit="Consulting", pet=pet1)
        v4 = Visit.objects.create(id=4, date_visit="2023-11-29", time_visit="11:00", type_visit="", pet=pet1)

        # Create vaccination
        vc1 = Vaccination.objects.create(id=1, date_vaccination="2023-11-30", type_vaccination="DA2PPL", next_vaccination="2024-11-30", details="The dog feels good", vet="D-r Brown", pet=pet2)
        vc2 = Vaccination.objects.create(id=2, date_vaccination="2023-11-30", type_vaccination="Nobivac® Tricat Trio", next_vaccination="2024-11-30", details="The dog feels good", vet="", pet=pet2)
        vc3 = Vaccination.objects.create(id=3, date_vaccination="2023-11-30", type_vaccination="", next_vaccination="2024-11-30", details="The dog feels good", vet="D-r Brown", pet=pet2)

     
    def test_valid_user(self):
        user = User.objects.get(id=1)
        self.assertTrue(user.is_valid_user())
        
    def test_invalid_user(self):
        user3 = User.objects.get(id=3)
        self.assertFalse(user3.is_valid_user())
        user4 = User.objects.get(id=4)
        self.assertFalse(user4.is_valid_user())
           
    def test_valid_pet(self):
        pet = Pet.objects.get(id=1)
        self.assertTrue(pet.is_valid_pet())
        
    def test_invalid_pet(self):
        pet = Pet.objects.get(id=3)
        self.assertFalse(pet.is_valid_pet())
        
    def test_is_valid_insurance(self):
        insurance = Insurance.objects.get(id=1)
        self.assertTrue(insurance.is_valid_insurance())
    
    def test_invalid_insurance(self):
        insurance = Insurance.objects.get(id=3)
        self.assertFalse(insurance.is_valid_insurance())
        
    def test_is_valid_visit(self):
        visit = Visit.objects.get(id=2)
        self.assertTrue(visit.is_valid_visit())
        
    def test_invalid_visit(self):
        visit3 = Visit.objects.get(id=3)
        self.assertFalse(visit3.is_valid_visit())
        visit4 = Visit.objects.get(id=4)
        self.assertFalse(visit4.is_valid_visit())
        
    def test_is_valid_vaccination(self):
        vaccination = Vaccination.objects.get(id=1)
        self.assertTrue(vaccination.is_valid_vaccination())
        
    def test_invalid_vaccination(self):
        vaccination2 = Vaccination.objects.get(id=2)
        self.assertFalse(vaccination2.is_valid_vaccination())
        vaccination3 = Vaccination.objects.get(id=3)
        self.assertFalse(vaccination3.is_valid_vaccination())
        
        
class PetclinicUITestCase(TestCase):
    
    def setUp(self):
    
        # Create users.
        a1 = User.objects.create(id=1, username=123, identical_number=123, first_name="a", last_name="b", phone_number="010-1002030")
        a1.set_password('12345')
        a1.save()
        a2 = User.objects.create(id=2, username=987, identical_number=987, first_name="z", last_name="y", phone_number="011-1002132")
        a2.set_password('98765')
        a2.save()
        
        # Create pets.
        pet1 = Pet.objects.create(id=1, icon="🐰", nickname="Ted", birth_date="2018-02-07", pet_type="Cat", details="ragdoll", owner=a1)
        pet2 = Pet.objects.create(id=2, icon="🐶", nickname="Jojo", birth_date="2020-12-25", pet_type="Dog", details="papillon", owner=a1)
        pet3 = Pet.objects.create(id=3, icon="🐹", nickname="Dora", birth_date="2022-11-05", pet_type="Hamster", details="Cricetulus", owner=a1)
        pet4 = Pet.objects.create(id=4, icon="🐕‍🦺", nickname="Arno", birth_date="2019-03-18", pet_type="Dog", details="Collie", owner=a2)

        # Create insurance.
        i1 = Insurance.objects.create(id=1, start_date="2023-11-18", monthly_price=25, owner=a1, pet=pet1)
        i2 = Insurance.objects.create(id=2, start_date="2023-11-20", monthly_price=30, owner=a1, pet=pet2)
        i3 = Insurance.objects.create(id=3, start_date="2023-11-21", monthly_price=15, owner=a1, pet=pet3)
        i4 = Insurance.objects.create(id=4, start_date="2023-11-24", monthly_price=30, owner=a2, pet=pet4)
    
        # Create visit.
        v1 = Visit.objects.create(id=1, date_visit="2023-11-20", time_visit="09:30", type_visit="Consulting", pet=pet1)
        v2 = Visit.objects.create(id=2, date_visit="2023-11-21", time_visit="16:00", type_visit="Vaccination", pet=pet1)
        v3 = Visit.objects.create(id=3, date_visit="2023-11-25", time_visit="17:30", type_visit="Consulting", pet=pet2)
        v4 = Visit.objects.create(id=4, date_visit="2023-11-27", time_visit="18:00", type_visit="Vaccination", pet=pet2)
        v5 = Visit.objects.create(id=5, date_visit="2023-11-28", time_visit="11:00", type_visit="Illness", pet=pet3)
        v6 = Visit.objects.create(id=6, date_visit="2023-11-25", time_visit="16:30", type_visit="Consulting", pet=pet4)

        # Create vaccination
        vc1 = Vaccination.objects.create(id=1, date_vaccination="2023-11-21", type_vaccination="Nobivac® Tricat Trio", next_vaccination="2024-11-21", details="The cat feels good", vet="D-r Mitchell", pet=pet1)
        vc2 = Vaccination.objects.create(id=2, date_vaccination="2023-11-27", type_vaccination="DA2PPL", next_vaccination="2024-11-27", details="The dog is healthy", vet="D-r Brown", pet=pet2)
       
    # Check if page login loads
    def test_login_page(self):
        c = Client()
        response = c.get("/login")
        self.assertEqual(response.status_code, 200)
    
    # Check if user can logged in    
    def test_login(self):
        c = Client()    
        logged_in = c.login(username='123', password='12345')
        self.assertTrue(logged_in) 
        
    # Check the visit page for logged in user
    def test_visit_page(self):
        c = Client()
        logged_in = c.login(username='123', password='12345')
        self.assertTrue(logged_in) 
        response = c.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["type_visit_options"]), 3)
        self.assertEqual(len(response.context["pets"]), 3)
        
    # Check the vaccination page for logged in user
    def test_vaccination_page(self):
        c = Client()
        logged_in = c.login(username='123', password='12345')
        self.assertTrue(logged_in) 
        response = c.get("/show_vaccinations")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["list_vaccinations"]), 2)
        self.assertEqual(len(response.context["pets_without_vaccination"]), 1)
        
    # Check the pet insurance for pet for logged in user
    def test_pet_insurance_page(self):
        c = Client()
        logged_in = c.login(username="123", password="12345")
        self.assertTrue(logged_in)
        response = c.get("/pet_insurance/1")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["pet"], "Ted")
        self.assertTrue(response.context["monthly_price"], 25)
        self.assertTrue(response.context["pet"].pet_type, "Cat")
    
    # Check the register pet page for logged in user
    def test_add_pet_page(self):
        c = Client()
        logged_in = c.login(username="123", password="12345")
        self.assertTrue(logged_in)
        response = c.get("/add_pet")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["pets"], 3)
      
    # Check the notification page for logged in user
    def test_notification_page(self):
        c = Client()
        logged_in = c.login(username='123', password='12345')
        self.assertTrue(logged_in)
        response = c.get("/notification")
        self.assertEqual(len(response.context["pets_visits"]), 5)   