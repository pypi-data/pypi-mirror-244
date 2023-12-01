import unittest
from nttinject import *


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


class InjectTest(unittest.TestCase):
    def test_pass(self):
        injector = Injector()
        injector.AddSingleton(Model, lambda: Model("Test"))
        injector.AddTransient(ViewModel, lambda: ViewModel("Test View Model"))

        view = View()
        View()

        self.assertEqual(
            view._model.GetModelInstances(), 1
        )

        self.assertEqual(
            view._viewModel.GetModelInstances(), 2
        )