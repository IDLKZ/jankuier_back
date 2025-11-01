"""
Locust Load Testing Configuration for Jankuier Backend API

Этот файл содержит сценарии нагрузочного тестирования для всех основных
эндпоинтов FastAPI приложения.

Запуск:
    # Web UI mode (рекомендуется)
    locust --host=http://localhost:8000

    # Headless mode
    locust --host=http://localhost:8000 --users 100 --spawn-rate 10 --run-time 60s --headless

    # Конкретный test case
    locust --host=http://localhost:8000 AuthUser
"""

import json
import random
from locust import HttpUser, task, between, SequentialTaskSet, TaskSet


class PublicAPIUser(HttpUser):
    """
    Симуляция пользователя, работающего с публичными API (без аутентификации).
    Тестирует справочные данные: города, страны, виды спорта.
    """
    wait_time = between(1, 3)
    weight = 3

    @task(3)
    def get_cities(self):
        """Получение списка городов (часто используемый эндпоинт)"""
        self.client.get("/api/city/all", name="/api/city/all")

    @task(3)
    def get_cities_paginated(self):
        """Получение городов с пагинацией"""
        page = random.randint(1, 5)
        self.client.get(
            f"/api/city/?page={page}&per_page=20",
            name="/api/city/ [paginated]"
        )

    @task(2)
    def get_countries(self):
        """Получение списка стран"""
        self.client.get("/api/country/all", name="/api/country/all")

    @task(2)
    def get_sports(self):
        """Получение списка видов спорта"""
        self.client.get("/api/sport/all", name="/api/sport/all")

    @task(1)
    def get_city_by_id(self):
        """Получение конкретного города по ID"""
        city_id = random.randint(1, 50)
        self.client.get(
            f"/api/city/get/{city_id}",
            name="/api/city/get/[id]"
        )

    @task(1)
    def get_country_by_id(self):
        """Получение конкретной страны по ID"""
        country_id = random.randint(1, 20)
        self.client.get(
            f"/api/country/get/{country_id}",
            name="/api/country/get/[id]"
        )


class AuthenticationFlow(SequentialTaskSet):
    """
    Последовательный сценарий: регистрация -> логин -> получение профиля.
    Используется для тестирования полного цикла аутентификации.
    """

    def on_start(self):
        """Инициализация данных пользователя"""
        self.username = f"test_user_{random.randint(1000, 9999)}"
        self.password = "TestPassword123!"
        self.access_token = None

    @task
    def register(self):
        """Регистрация нового пользователя"""
        payload = {
            "username": self.username,
            "password": self.password,
            "email": f"{self.username}@test.com",
            "phone": f"77{random.randint(700000000, 799999999)}",
            "iin": f"{random.randint(100000000000, 999999999999)}",  # 12-digit IIN
            "first_name": "Test",
            "last_name": "User",
            "patronomic": None,
            "role_id": 2  # Client role
        }

        with self.client.post(
            "/api/auth/register",
            json=payload,
            catch_response=True,
            name="/api/auth/register"
        ) as response:
            if response.status_code == 201 or response.status_code == 200:
                response.success()
            elif response.status_code == 400:
                # Пользователь уже существует - не критично для нагрузочного теста
                response.success()
            else:
                response.failure(f"Got status code {response.status_code}")

    @task
    def login(self):
        """Авторизация пользователя"""
        payload = {
            "username": self.username,
            "password": self.password
        }

        with self.client.post(
            "/api/auth/login-client",
            json=payload,
            catch_response=True,
            name="/api/auth/login-client"
        ) as response:
            if response.status_code == 200:
                try:
                    data = response.json()
                    self.access_token = data.get("access_token")
                    response.success()
                except json.JSONDecodeError:
                    response.failure("Response is not valid JSON")
            else:
                response.failure(f"Login failed with status {response.status_code}")

    @task
    def get_profile(self):
        """Получение данных авторизованного пользователя"""
        if not self.access_token:
            return

        headers = {"Authorization": f"Bearer {self.access_token}"}
        self.client.get(
            "/api/auth/me",
            headers=headers,
            name="/api/auth/me"
        )

    @task
    def stop(self):
        """Завершение последовательности"""
        self.interrupt()


class AuthUser(HttpUser):
    """
    Пользователь с аутентификацией, выполняющий последовательность операций.
    """
    wait_time = between(2, 5)
    weight = 2
    tasks = [AuthenticationFlow]


class ProductBrowserUser(HttpUser):
    """
    Симуляция пользователя, просматривающего товары и работающего с корзиной.
    Требует предварительной аутентификации.
    """
    wait_time = between(1, 4)
    weight = 2

    def on_start(self):
        """Логин перед началом работы"""
        self.access_token = None
        self.login()

    def login(self):
        """Аутентификация с тестовым пользователем"""
        payload = {
            "username": "client",  # Из seeder
            "password": "Client123!"
        }

        with self.client.post(
            "/api/auth/login-client",
            json=payload,
            catch_response=True
        ) as response:
            if response.status_code == 200:
                try:
                    data = response.json()
                    self.access_token = data.get("access_token")
                except json.JSONDecodeError:
                    pass

    @property
    def headers(self):
        """Возвращает заголовки с токеном авторизации"""
        if self.access_token:
            return {"Authorization": f"Bearer {self.access_token}"}
        return {}

    @task(4)
    def browse_products(self):
        """Просмотр списка товаров"""
        page = random.randint(1, 5)
        self.client.get(
            f"/api/product/?page={page}&per_page=20",
            headers=self.headers,
            name="/api/product/ [browse]"
        )

    @task(2)
    def view_product_details(self):
        """Просмотр деталей конкретного товара"""
        product_id = random.randint(1, 100)
        self.client.get(
            f"/api/product/get/{product_id}",
            headers=self.headers,
            name="/api/product/get/[id]"
        )

    @task(3)
    def browse_product_categories(self):
        """Просмотр категорий товаров"""
        self.client.get(
            "/api/product-category/all",
            headers=self.headers,
            name="/api/product-category/all"
        )

    @task(1)
    def view_cart(self):
        """Просмотр корзины"""
        if not self.access_token:
            return

        self.client.get(
            "/api/cart/my-cart",
            headers=self.headers,
            name="/api/cart/my-cart"
        )


class AcademyBrowserUser(HttpUser):
    """
    Симуляция пользователя, работающего с академиями и группами.
    """
    wait_time = between(2, 4)
    weight = 2

    @task(3)
    def browse_academies(self):
        """Просмотр списка академий"""
        self.client.get("/api/academy/all", name="/api/academy/all")

    @task(2)
    def view_academy_details(self):
        """Просмотр деталей академии"""
        academy_id = random.randint(1, 20)
        self.client.get(
            f"/api/academy/get/{academy_id}",
            name="/api/academy/get/[id]"
        )

    @task(2)
    def browse_academy_groups(self):
        """Просмотр групп академий"""
        page = random.randint(1, 3)
        self.client.get(
            f"/api/academy-group/?page={page}&per_page=20",
            name="/api/academy-group/ [paginated]"
        )

    @task(1)
    def view_group_schedule(self):
        """Просмотр расписания группы"""
        self.client.get(
            "/api/academy-group-schedule/all",
            name="/api/academy-group-schedule/all"
        )


class FieldBrowserUser(HttpUser):
    """
    Симуляция пользователя, работающего с полями и площадками.
    """
    wait_time = between(2, 4)
    weight = 2

    @task(4)
    def browse_fields(self):
        """Просмотр списка полей"""
        page = random.randint(1, 5)
        self.client.get(
            f"/api/field/?page={page}&per_page=20",
            name="/api/field/ [browse]"
        )

    @task(2)
    def view_field_details(self):
        """Просмотр деталей поля"""
        field_id = random.randint(1, 50)
        self.client.get(
            f"/api/field/get/{field_id}",
            name="/api/field/get/[id]"
        )

    @task(2)
    def browse_field_parties(self):
        """Просмотр площадок полей"""
        self.client.get(
            "/api/field-party/all",
            name="/api/field-party/all"
        )

    @task(1)
    def view_field_schedule(self):
        """Просмотр расписания площадки"""
        self.client.get(
            "/api/field-party-schedule/all",
            name="/api/field-party-schedule/all"
        )


class AdminOperationsUser(HttpUser):
    """
    Симуляция администратора, выполняющего административные операции.
    Требует логина с правами администратора.
    """
    wait_time = between(3, 6)
    weight = 1

    def on_start(self):
        """Логин администратора"""
        self.access_token = None
        self.login_as_admin()

    def login_as_admin(self):
        """Аутентификация администратора"""
        payload = {
            "username": "admin",  # Из seeder
            "password": "Admin123!"
        }

        with self.client.post(
            "/api/auth/login",
            json=payload,
            catch_response=True
        ) as response:
            if response.status_code == 200:
                try:
                    data = response.json()
                    self.access_token = data.get("access_token")
                except json.JSONDecodeError:
                    pass

    @property
    def headers(self):
        """Возвращает заголовки с токеном авторизации"""
        if self.access_token:
            return {"Authorization": f"Bearer {self.access_token}"}
        return {}

    @task(2)
    def view_users(self):
        """Просмотр списка пользователей"""
        if not self.access_token:
            return

        self.client.get(
            "/api/user/all",
            headers=self.headers,
            name="/api/user/all [admin]"
        )

    @task(2)
    def view_roles(self):
        """Просмотр ролей"""
        if not self.access_token:
            return

        self.client.get(
            "/api/role/all",
            headers=self.headers,
            name="/api/role/all [admin]"
        )

    @task(1)
    def view_permissions(self):
        """Просмотр разрешений"""
        if not self.access_token:
            return

        self.client.get(
            "/api/permission/all",
            headers=self.headers,
            name="/api/permission/all [admin]"
        )

    @task(1)
    def view_orders(self):
        """Просмотр заказов (админ)"""
        if not self.access_token:
            return

        page = random.randint(1, 3)
        self.client.get(
            f"/api/product-order-admin/?page={page}&per_page=20",
            headers=self.headers,
            name="/api/product-order-admin/ [admin]"
        )


class MixedOperationsUser(HttpUser):
    """
    Симуляция реального пользователя со смешанными операциями.
    Комбинирует различные типы запросов в реалистичной пропорции.
    """
    wait_time = between(1, 5)
    weight = 4

    def on_start(self):
        """Инициализация пользователя"""
        self.access_token = None
        # 30% вероятность залогиниться
        if random.random() < 0.3:
            self.try_login()

    def try_login(self):
        """Попытка авторизации"""
        payload = {
            "username": "client",
            "password": "Client123!"
        }

        response = self.client.post("/api/auth/login-client", json=payload)
        if response.status_code == 200:
            try:
                data = response.json()
                self.access_token = data.get("access_token")
            except:
                pass

    @property
    def headers(self):
        """Возвращает заголовки с токеном авторизации"""
        if self.access_token:
            return {"Authorization": f"Bearer {self.access_token}"}
        return {}

    @task(5)
    def browse_public_data(self):
        """Просмотр публичных данных"""
        endpoints = [
            "/api/city/all",
            "/api/country/all",
            "/api/sport/all",
        ]
        endpoint = random.choice(endpoints)
        self.client.get(endpoint, name="[mixed] public data")

    @task(4)
    def browse_products_or_fields(self):
        """Просмотр товаров или полей"""
        choice = random.choice(["product", "field", "academy"])
        page = random.randint(1, 3)

        self.client.get(
            f"/api/{choice}/?page={page}&per_page=20",
            headers=self.headers,
            name=f"[mixed] browse {choice}"
        )

    @task(2)
    def view_details(self):
        """Просмотр деталей случайной сущности"""
        entity = random.choice(["product", "field", "academy"])
        entity_id = random.randint(1, 50)

        self.client.get(
            f"/api/{entity}/get/{entity_id}",
            headers=self.headers,
            name=f"[mixed] view {entity} details"
        )

    @task(1)
    def check_profile(self):
        """Проверка профиля (если залогинен)"""
        if not self.access_token:
            return

        self.client.get(
            "/api/auth/me",
            headers=self.headers,
            name="[mixed] check profile"
        )


# Дополнительные утилиты для custom тестов
class StressTestUser(HttpUser):
    """
    Экстремальный стресс-тест с максимальной нагрузкой.
    Использовать с осторожностью!

    Запуск:
        locust --host=http://localhost:8000 StressTestUser --users 500 --spawn-rate 50
    """
    wait_time = between(0.5, 1)
    weight = 1

    @task
    def rapid_fire_requests(self):
        """Быстрые последовательные запросы"""
        endpoints = [
            "/api/city/all",
            "/api/country/all",
            "/api/sport/all",
            "/api/product/",
            "/api/field/",
        ]

        for _ in range(3):
            endpoint = random.choice(endpoints)
            self.client.get(endpoint, name="[stress] rapid fire")
