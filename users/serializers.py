from rest_framework import serializers

from users.models import User, Location


FORBIDDEN_DOMAIN = "rambler.ru"


class EmailRamblerCheck:
    def __call__(self, value):
        if value.endswith(FORBIDDEN_DOMAIN):
            raise serializers.ValidationError(f"You can't use {FORBIDDEN_DOMAIN} domain")


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    locations = serializers.SlugRelatedField(
        read_only=True,
        many=True,
        slug_field="name"
    )

    class Meta:
        model = User
        exclude = ["password"]


class UserCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    locations = serializers.SlugRelatedField(
        required=False,
        queryset=Location.objects.all(),
        many=True,
        slug_field="name"
    )
    email = serializers.EmailField(validators=[EmailRamblerCheck()])

    def is_valid(self, raise_exception=False):
        self._locations = self.initial_data.pop("locations")
        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(user.password)

        for location in self._locations:
            loc_obj, _ = Location.objects.get_or_create(name=location)
            user.locations.add(loc_obj)

        user.save()
        return user

    class Meta:
        model = User
        fields = '__all__'


class UserUpdateSerializer(serializers.ModelSerializer):
    locations = serializers.SlugRelatedField(
        required=False,
        queryset=Location.objects.all(),
        many=True,
        slug_field="name"
    )
    email = serializers.EmailField(validators=[EmailRamblerCheck()])

    def is_valid(self, raise_exception=False):
        self._locations = self.initial_data.pop("locations")
        return super().is_valid(raise_exception=raise_exception)

    def save(self):
        user = super().save()

        for location in self._locations:
            loc_obj, _ = Location.objects.get_or_create(name=location)
            user.locations.add(loc_obj)

        user.save()
        return user

    class Meta:
        model = User
        fields = '__all__'


class UserDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id"]
