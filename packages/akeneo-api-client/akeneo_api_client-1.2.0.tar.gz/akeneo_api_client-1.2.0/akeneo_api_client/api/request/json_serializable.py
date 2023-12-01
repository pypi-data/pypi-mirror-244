import abc


class JsonSerializable(abc.ABC):

    @classmethod
    @abc.abstractmethod
    def serialize(self) -> str:
        pass
