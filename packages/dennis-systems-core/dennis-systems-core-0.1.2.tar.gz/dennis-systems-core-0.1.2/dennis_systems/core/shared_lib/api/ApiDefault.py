from django.db.models import Model

from dennis_systems.core.shared_lib.auth.Authorization import Authorization
from django.core import serializers
from django.http import JsonResponse, HttpRequest

from dennis_systems.core.shared_lib.entity.BaseModel import BaseModel
from dennis_systems.core.shared_lib.service.DefaultService import DefaultService


class ApiDefault:
    __service: DefaultService

    def list(self, request: HttpRequest, limit: int, page: int) -> JsonResponse:
        self.check_token(request)
        return JsonResponse(self.__service.list(limit, page))
        pass

    def save(self, item: Model, request: HttpRequest) -> JsonResponse:
        self.check_token(request)
        return self.to_result(self.get_service().save_item(item))


    def delete(self, request: HttpRequest, item: Model) -> JsonResponse:
        self.check_token(request)
        return JsonResponse(self.__service.delete(item))

    def get(self, request: HttpRequest, id: int) -> JsonResponse:
        self.check_token(request)
        return JsonResponse(self.__service.get(id), safe=False)

    def get_service(self):
        return self.__service

    def to_result(self, item: Model):
        return JsonResponse(serializers.serialize("json", item.objects.all()), safe=False)



    @staticmethod
    def to_model(model: BaseModel):
        return JsonResponse(model)

    @staticmethod
    def check_token(request: HttpRequest) -> None:
        if not Authorization.has_auth_token(request):
            print('not token')
        else:
            print('token_found')
            Authorization.parce_token(request)
