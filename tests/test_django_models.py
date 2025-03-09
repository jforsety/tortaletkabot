import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
from app_tortaletka.models import Client, BroadcastMessage


@pytest.mark.django_db
class TestClientModel:
    @pytest.fixture
    def client_instance(self):
        return Client.objects.create(external_id=123)

    def test_create_client(self, client_instance):
        """Тестирование создания клиента с обязательными полями"""
        assert Client.objects.count() == 1
        assert client_instance.external_id == 123

    def test_default_values(self, client_instance):
        """Проверка значений по умолчанию"""
        assert client_instance.attempt == 10
        assert client_instance.premium_status is False
        assert client_instance.referrals == 0

    def test_str_representation(self, client_instance):
        """Проверка строкового представления"""
        client_instance.first_name = "Иван"
        assert str(client_instance) == f"{client_instance.id} : Иван"

    def test_meta_options(self):
        """Проверка мета-опций модели"""
        assert Client._meta.verbose_name == "Пользователя бота"
        assert Client._meta.verbose_name_plural == "Пользователи бота"
        assert Client._meta.ordering == ["date_registration"]

    def test_auto_date_fields(self, client_instance):
        """Проверка автоматического заполнения дат"""
        assert client_instance.date_registration is not None
        assert client_instance.last_date is not None
        # Проверка, что last_date не обновляется при сохранении (auto_now_add=True)
        original_last_date = client_instance.last_date
        client_instance.save()
        assert client_instance.last_date == original_last_date


@pytest.mark.django_db
class TestBroadcastMessageModel:
    @pytest.fixture
    def broadcast_message(self):
        return BroadcastMessage.objects.create(title="Test Title")

    @pytest.fixture
    def client_instance(self):
        return Client.objects.create(external_id=456)

    def test_create_broadcast(self, broadcast_message):
        """Тестирование создания рассылки"""
        assert BroadcastMessage.objects.count() == 1
        assert broadcast_message.title == "Test Title"

    def test_defaults(self, broadcast_message):
        """Проверка значений по умолчанию"""
        assert broadcast_message.content_type == "text"
        assert broadcast_message.sent is False

    def test_str_representation(self, broadcast_message):
        """Проверка строкового представления"""
        assert str(broadcast_message) == f"{broadcast_message.id} : Test Title"

    def test_content_type_choices(self):
        """Проверка доступных вариантов content_type"""
        content_type_field = BroadcastMessage._meta.get_field("content_type")
        expected_choices = [
            ("text", "Только текст"),
            ("image", "Только изображение"),
            ("both", "Текст + изображение"),
        ]
        assert content_type_field.choices == expected_choices

    def test_m2m_relationship(self, broadcast_message, client_instance):
        """Проверка связи ManyToMany с пользователями"""
        broadcast_message.users.add(client_instance)
        assert client_instance in broadcast_message.users.all()
        assert broadcast_message.users.count() == 1

    def test_image_upload(self):
        """Тестирование загрузки изображения"""
        image = SimpleUploadedFile(
            "test.jpg", b"file_content", content_type="image/jpeg"
        )
        broadcast = BroadcastMessage.objects.create(
            title="Image Test",
            content_type="image",
            image=image
        )
        assert broadcast.image.name.startswith("broadcast/")
        broadcast.image.delete(save=False)  # Очистка файла после теста

    def test_optional_fields(self, broadcast_message):
        broadcast_message.text = None
        broadcast_message.image = None
        broadcast_message.save()
        refreshed_message = BroadcastMessage.objects.get(pk=broadcast_message.pk)
        assert refreshed_message.text is None
        assert not refreshed_message.image  # Проверка через булево преобразование
        assert refreshed_message.image.name == ""  # Альтернативная проверка