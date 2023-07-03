# character.py

class Character:
    def __init__(self, x_pos=int, y_pos=int, path=str):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.path = path
        self.x_speed = 0
        self.y_speed = 0

    def set_speed(self, x_speed, y_speed):
        '''
        This method sets the enemy's moving speed
        (negative to left or bottom, postive to right or up)
        speed is by default zero
        '''
        self.x_speed = x_speed
        self.y_speed = y_speed

    def set_pos(self, x_pos, y_pos):
        '''
        This method sets the postion manually
        '''
        self.x_pos = x_pos
        self.y_pos = y_pos

    def update_pos(self):
        '''
        This method updates the position of this enemy object according to its speed
        '''
        self.x_pos += self.x_speed
        self.y_pos += self.y_speed

    def get_pos(self):
        '''
        This method returns the enemy postion in a tuple
        '''

        return (self.x_pos, self.y_pos)

    def get_path(self):
        '''
        This method returns the path of this enemy object (the image)
        '''

        return self.path


class Enemy(Character):
    '''
    This class creates an enemy object
    '''

    def __init__(self, x_pos=int, y_pos=int, path=str):
        super().__init__(x_pos, y_pos, path)


class Player(Character):

    def __init__(self, x_pos, y_pos, path):
        super().__init__(x_pos, y_pos, path)

    def jump(self, delta_y, ground):

        if ground == self.y_pos:
            self.set_pos(self.x_pos, self.y_pos + delta_y)

    def gravity(self, acceleration=-9.8, time=1, ground=0):

        if self.y_pos < ground:

            speed = time * acceleration
            self.y_pos += speed

        else:
            self.y_pos = ground


def test():
    player1 = Player(0, 0, "test")
    player1.jump(80)
    print(player1.get_pos())


if __name__ == "__main__":

    test()
