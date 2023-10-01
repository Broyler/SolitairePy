from components import object, scale


class Stack(object.Object):
    scale = scale.Scale(scale.ScaleModes.INHERIT, 1.0)
    width = scale.apply(0)
    height = scale.apply(0)
    objects = []

    def __init__(self, objects, position_policy):
        self.objects = objects
        self.position_policy = position_policy
        super().__init__()

    def draw(self):
        for i in self.objects:
            i.draw()
