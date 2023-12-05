from typing import Sequence, Generator, Any
from entropic.sources import Iteration
from entropic.db import default_database


class Results:
    database = default_database()
    iteration = Iteration

    def _load(self, document_list: Sequence[dict]) -> Generator[Any, None, None]:
        for document in document_list:
            yield self.iteration.model_validate(document)

    @property
    def all(self) -> Generator[Any, None, None]:
        return self._load(self.database.all())

    def filter(self, **kwargs) -> Generator[Any, None, None]:
        return self._load(self.database.filter(**kwargs))

    def get(self, **kwargs):
        if item := self.database.get(**kwargs):
            return self.iteration.model_validate(item)
        return None

    def set_iteration(self, iteration_class):
        """Change the default iteration to be used for loading results"""
        self.iteration = iteration_class
