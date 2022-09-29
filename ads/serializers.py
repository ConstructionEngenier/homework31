from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from ads.models import Selection, Ad, Category
from users.models import User


class NotTrueValidator:
    def __call__(self, value):
        if value:
            raise serializers.ValidationError("New add can't be published")


class AdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = '__all__'


class AdCreateSerializer(serializers.ModelSerializer):
    is_published = serializers.BooleanField(validators=[NotTrueValidator()])
    author = serializers.StringRelatedField(read_only=True)
    category = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Ad
        fields = "__all__"

    def is_valid(self, raise_exception=True):
        self._author_id = self.initial_data.pop("author")
        self._category_id = self.initial_data.pop("category")
        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        validated_data['author'] = get_object_or_404(User.objects, id=self._author_id)
        validated_data['category'] = get_object_or_404(Category.objects, id=self._category_id)

        ad = Ad.objects.create(**validated_data)
        return ad


class AdDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = ["id"]


class SelectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Selection
        fields = ["id", "name"]


class SelectionDetailSerializer(serializers.ModelSerializer):
    items = serializers.SlugRelatedField(
        read_only=True,
        many=True,
        slug_field="name"
    )
    owner = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Selection
        fields = "__all__"


class SelectionCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    items = serializers.SlugRelatedField(
        required=False,
        many=True,
        queryset=Ad.objects.all(),
        slug_field="id"
    )

    class Meta:
        model = Selection
        fields = "__all__"

    def is_valid(self, raise_exception=True):
        self._items = self.initial_data.pop("items")
        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        items = []
        for item in self._items:
            item_obj = get_object_or_404(Ad.objects, id=item)
            items.append(item_obj)

        selection = Selection.objects.create(**validated_data)

        for item in items:
            selection.items.add(item)

        selection.save()
        return selection


class SelectionUpdateSerializer(serializers.ModelSerializer):
    items = serializers.SlugRelatedField(
        required=False,
        many=True,
        queryset=Ad.objects.all(),
        slug_field="name"
    )

    class Meta:
        model = Selection
        fields = "__all__"

    def is_valid(self, raise_exception=True):
        self._items = self.initial_data.pop("items")
        return super().is_valid(raise_exception=raise_exception)

    def save(self):
        selection = super().save()

        for item in self._items:
            item_obj = get_object_or_404(Ad.objects, id=item)
            selection.items.add(item_obj)

        selection.save()
        return selection


class SelectionDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Selection
        fields = ["id"]
