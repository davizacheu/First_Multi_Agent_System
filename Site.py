class Site:
    def __init__(self, x_coordinate, y_coordinate) -> None:
        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate

class Foreign_Site(Site):
    def __init__(self, x_coordinate, y_coordinate, quality) -> None:
        super().__init__(x_coordinate, y_coordinate)
        self.quality = quality
        