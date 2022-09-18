import pandas
from django.http import JsonResponse
from django.views import View

from ads.models import Ad, Category
from users.models import User, Location


class AddAdsData(View):
    def get(self, request):
        data_ads = pandas.read_csv('/Users/artem/Artems documents/Python/lesson28/homework28/data/ad.csv',
                                   sep=',').to_dict()

        i = 0
        while max(data_ads['Id'].values()) > i:
            ad = Ad.objects.create(
                name=data_ads["name"][i],
                author_id=data_ads["author_id"][i],
                price=data_ads["price"][i],
                description=data_ads["description"][i],
                is_published=data_ads["is_published"][i],
                image=data_ads["image"][i],
                category_id=data_ads["category_id"][i],
            )
            i += 1
        return JsonResponse("Advertising data upload successful", safe=False, status=200)


class AddCatData(View):
    def get(self, request):
        data_cat = pandas.read_csv('/Users/artem/Artems documents/Python/lesson28/homework28/data/category.csv',
                                   sep=',').to_dict()

        i = 0
        while max(data_cat['id'].values()) > i:
            cat = Category.objects.create(
                name=data_cat["name"][i],
            )
            i += 1
        return JsonResponse("Category data upload successful", safe=False, status=200)


class AddLocData(View):
    def get(self, request):
        data_loc = pandas.read_csv('/Users/artem/Artems documents/Python/lesson28/homework28/data/location.csv',
                                   sep=',').to_dict()

        i = 0
        while max(data_loc['id'].values()) > i:
            loc = Location.objects.create(
                name=data_loc["name"][i],
                lat=data_loc["lat"][i],
                lng=data_loc["lng"][i],
            )
            i += 1
        return JsonResponse("Location data upload successful", safe=False, status=200)


class AddUserData(View):
    def get(self, request):
        data_user = pandas.read_csv('/Users/artem/Artems documents/Python/lesson28/homework28/data/user.csv',
                                    sep=',').to_dict()
        i = 0
        while max(data_user['id'].values()) > i:
            user = User.objects.create(
                first_name=data_user["first_name"][i],
                last_name=data_user["last_name"][i],
                username=data_user["username"][i],
                password=data_user["password"][i],
                role=data_user["role"][i],
                age=data_user["age"][i],
            )
            i += 1
        return JsonResponse("User data upload successful", safe=False, status=200)
