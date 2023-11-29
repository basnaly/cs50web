from django.test import TestCase, Client

from .models import User, Pet, Insurance, Visit, Vaccination

# Create your tests here.

class PetclinicTestCase(TestCase):
    
    def setUp(self):
    
        # Create users.
        a1 = User.objects.create(id=1, username=123, identical_number=123, first_name="a", last_name="b", phone_number="010-1002030")
        a2 = User.objects.create(id=2, username=987, identical_number=987, first_name="c", last_name="d", phone_number="010-2005070")
        a3 = User.objects.create(id=3, username=0, identical_number=0, first_name="e", last_name="f", phone_number="")
        a4 = User.objects.create(id=4, username=234, identical_number=234, first_name="e", last_name="", phone_number="010-2005080")

        # Create pets.
        pet1 = Pet.objects.create(id=1, icon="🐰", nickname="Ted", birth_date="2018-02-07", pet_type="cat", details="ragdoll", owner=a1)
        pet2 = Pet.objects.create(id=2, icon="🐶", nickname="Jojo", birth_date="2020-12-25", pet_type="dog", details="papillon", owner=a2)
        pet3 = Pet.objects.create(id=3, icon="🐩", nickname="", birth_date="2019-11-05", pet_type="dog", details="", owner=a2)

        # Create insurance.
        i1 = Insurance.objects.create(id=1, start_date="2023-12-01", monthly_price="25", owner=a1, pet=pet1)
        i2 = Insurance.objects.create(id=2, start_date="2023-11-29", monthly_price="30", owner=a2, pet=pet2)
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