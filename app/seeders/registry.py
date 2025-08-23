from app.seeders.role.role_seeder import RoleSeeder
from app.seeders.user.user_seeder import UserSeeder

seeders = [
    RoleSeeder(),
    UserSeeder(),
]
