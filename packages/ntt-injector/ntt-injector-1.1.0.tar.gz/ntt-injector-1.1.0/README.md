# Library for creating Dependency Injection Pattern

## Usage

``` python
from nttinjector import dependency_inject, Injector

class Model:
    count = 0

    def __init__(self, strName: str = "") -> None:
        self._strName = strName
        self.CreateNewModel()

    def __repr__(self) -> str:
        return f"<Model name=\"{self._strName}\" />"

    @classmethod
    def CreateNewModel(cls):
        cls.count += 1

    @classmethod
    def GetModelInstances(cls):
        return cls.count


@dependency_inject(Model)
class ViewModel:
    count = 0

    def __init__(self, mModel: Model, strName: str = "") -> None:
        self._mModel = mModel
        self._strName = strName
        self.CreateNewModel()

    @classmethod
    def CreateNewModel(cls):
        cls.count += 1

    @classmethod
    def GetModelInstances(cls):
        return cls.count

    def __repr__(self) -> str:
        return f"<ViewModel name=\"{self._strName}\" />"


@dependency_inject(ViewModel, Model)
class View:
    def __init__(self, viewModel: ViewModel, mModel: Model, strName: str = "") -> None:
        self._viewModel = viewModel
        self._model = mModel
        self._strName = strName

    def __repr__(self) -> str:
        return f"<View name=\"{self._strName}\" />"
```

Then use the View as normal

``` python
view = View()

print(view._model)
```