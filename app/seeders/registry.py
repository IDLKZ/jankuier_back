from app.seeders.city.city_seeder import CitySeeder
from app.seeders.country.country_seeder import CountrySeeder
from app.seeders.role.role_seeder import RoleSeeder
from app.seeders.sport.sport_seeder import SportSeeder
from app.seeders.user.user_seeder import UserSeeder

seeders = [
    RoleSeeder(),
    UserSeeder(),
    CountrySeeder(),
    SportSeeder(),
    CitySeeder(),
]
