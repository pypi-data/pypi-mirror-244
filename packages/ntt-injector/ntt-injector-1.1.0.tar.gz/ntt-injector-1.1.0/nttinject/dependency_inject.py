from .Injector import Injector


# def dependency_inject(*claDependencies):
#     def classDecorator(cls):
#         def decorator(*args, **kwargs):
#             injector = Injector()
#             objects = [
#                 injector.Get(claDependency) for claDependency in claDependencies
#             ]

#             return cls(*objects, *args, **kwargs)

#         return decorator
#     return classDecorator

def dependency_inject(*claDependencies):
    def classDecorator(cls):
        class WrappedClass(cls):
            def __init__(self, *args, **kwargs):
                injector = Injector()
                objects = [
                    injector.Get(claDependency) for claDependency in claDependencies
                ]

                super().__init__(*objects, *args, **kwargs)

        return WrappedClass
    return classDecorator