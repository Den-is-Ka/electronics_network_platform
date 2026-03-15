from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import models


class NetworkNode(models.Model):
    class NodeType(models.TextChoices):
        FACTORY = "factory", "Завод"
        RETAIL = "retail", "Розничная сеть"
        ENTREPRENEUR = "entrepreneur", "Индивидуальный предприниматель"

    name = models.CharField(max_length=255, verbose_name="Название")
    node_type = models.CharField(
        max_length=20,
        choices=NodeType.choices,
        verbose_name="Тип звена",
    )
    email = models.EmailField(verbose_name="Email")
    country = models.CharField(max_length=100, verbose_name="Страна")
    city = models.CharField(max_length=100, verbose_name="Город")
    street = models.CharField(max_length=255, verbose_name="Улица")
    house_number = models.CharField(max_length=20, verbose_name="Номер дома")
    supplier = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="clients",
        verbose_name="Поставщик",
    )
    debt = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
        verbose_name="Задолженность перед поставщиком",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Время создания",
    )

    class Meta:
        verbose_name = "Звено сети"
        verbose_name_plural = "Звенья сети"
        ordering = ("id",)

    def __str__(self):
        return self.name

    @property
    def hierarchy_level(self):
        level = 0
        current = self.supplier
        visited = set()

        while current:
            if current.pk in visited:
                break
            visited.add(current.pk)
            level += 1
            current = current.supplier

        return level

    def clean(self):
        errors = {}

        if self.supplier and self.pk and self.supplier.pk == self.pk:
            errors["supplier"] = "Объект сети не может ссылаться сам на себя."

        if self.node_type == self.NodeType.FACTORY and self.supplier is not None:
            errors["supplier"] = "Завод не может иметь поставщика."

        if self.node_type != self.NodeType.FACTORY and self.supplier is None:
            errors["supplier"] = "Для не-завода поставщик обязателен."

        visited = set()
        current = self.supplier
        level = 0

        if self.pk:
            visited.add(self.pk)

        while current:
            if current.pk in visited:
                errors["supplier"] = "Обнаружен циклический путь в иерархии."
                break

            visited.add(current.pk)
            level += 1

            if level > 2:
                errors["supplier"] = "Иерархия сети не может быть глубже 3 уровней."
                break

            current = current.supplier

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class Product(models.Model):
    network_node = models.ForeignKey(
        NetworkNode,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="Звено сети",
    )
    name = models.CharField(max_length=255, verbose_name="Название")
    model = models.CharField(max_length=255, verbose_name="Модель")
    release_date = models.DateField(verbose_name="Дата выхода продукта на рынок")

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ("id",)

    def __str__(self):
        return f"{self.name} ({self.model})"