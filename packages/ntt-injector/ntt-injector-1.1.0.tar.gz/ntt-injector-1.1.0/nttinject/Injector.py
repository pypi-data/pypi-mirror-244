from typing import (
    Any,
    Callable,
)


class Injector:
    _dictSingletons = {}
    _dictTransitions = {}

    @classmethod
    def AddSingleton(cls, claObjectClass: Callable, lamCreateObjectDef: Callable) -> None:
        cls._dictSingletons[claObjectClass] = lamCreateObjectDef()

    @classmethod
    def AddTransient(cls, claObjectClass: Callable, lamCreateObjectDef: Callable) -> None:
        cls._dictTransitions[claObjectClass] = lamCreateObjectDef

    @classmethod
    def Get(cls, claObjectClass: Callable) -> Any:
        if claObjectClass in cls._dictSingletons:
            return cls._dictSingletons[claObjectClass]
        elif claObjectClass in cls._dictTransitions:
            return cls._dictTransitions[claObjectClass]()
        else:
            raise Exception(f"The {claObjectClass} is not registered.")
