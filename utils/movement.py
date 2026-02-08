class MovementStrategy:
    def move(self, character):
        pass

class MoveLeft(MovementStrategy):
    def move(self, character):
        character.x -= character.speed

class MoveRight(MovementStrategy):
    def move(self, character):
        character.x += character.speed
