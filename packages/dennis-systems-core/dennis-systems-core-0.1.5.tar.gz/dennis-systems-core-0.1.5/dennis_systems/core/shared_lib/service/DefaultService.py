from typing import List, Optional

from django.db.models import Model


class DefaultService:
    def list(self, limit: int, page: int) -> List[Model]:
        pass

    def save(self, item: Model) -> Model:
        return self.save_item(item)
        pass

    def delete(self, item: Model) -> Model:
        pass

    def get(self, id: int) -> Optional[Model]:
        pass

    def save_item(self, item: Model) -> Model:
        item.save()
        return item
