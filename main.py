import pygame, sys
import random as r


# ==========================================================================================

class Room:
    def __init__(self, x, y, width, height, type):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.type = type


class Road:
    def __init__(self, x, y, dx, dy, type):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.type = type


class TreeNode:
    def __init__(self, x, y, width, height):
        self.left_tree = None  # TreeNode
        self.right_tree = None  # TreeNode
        self.parent_tree = None  # TreeNode
        self.tree_size = Room(x, y, width, height, None)
        self.dungeon_size = None  # RectInt


class Dungeon:
    map_size_x = 500
    map_size_y = 500

    root_node = None
    max_node = 5
    min_divide_size = 0.2
    max_divide_size = 0.8

    rooms = []
    roads = []

    @classmethod
    def Make_dungeon(cls, size, count):
        cls.map_size_x = size[0]
        cls.map_size_y = size[1]
        cls.max_node = count
        cls.rooms.clear()
        cls.roads.clear()

        cls.root_node = TreeNode(0, 0, cls.map_size_x, cls.map_size_y)
        cls.divide_tree(cls.root_node, 0)
        cls.generate_room(cls.root_node, 0)
        cls.generate_road(cls.root_node, 0)

    @classmethod
    def get_center_X(cls, size):
        return size.x + int(size.width/2)

    @classmethod
    def get_center_Y(cls, size):
        return size.y + int(size.height / 2)

    @classmethod
    def divide_tree(cls, tree_node, n):
        if n < cls.max_node:
            size = tree_node.tree_size
            length = size.width if size.width >= size.height else size.height
            split = r.randrange(int(length * cls.min_divide_size), int(length * cls.max_divide_size))
            if size.width >= size.height:
                tree_node.left_tree = TreeNode(size.x, size.y, split, size.height)
                tree_node.right_tree = TreeNode(size.x + split, size.y, size.width - split, size.height)
            else:
                tree_node.left_tree = TreeNode(size.x, size.y, size.width, split)
                tree_node.right_tree = TreeNode(size.x, size.y + split, size.width, size.height - split)
            tree_node.left_tree.parent_tree = tree_node
            tree_node.right_tree.parent_tree = tree_node

            cls.divide_tree(tree_node.left_tree, n + 1)
            cls.divide_tree(tree_node.right_tree, n + 1)

    @classmethod
    def generate_room(cls, tree_node, n):
        if n == cls.max_node:
            size = tree_node.tree_size
            width = r.randrange(int(size.width / 2), size.width - 1)
            height = r.randrange(int(size.height / 2), size.height - 1)
            x = size.x + r.randrange(1, size.width - width)
            y = size.y + r.randrange(1, size.height - height)
            type = None
            if r.randint(0, 0) == 0:
                type = pygame.transform.scale(Room1, (width, height))
            cls.rooms.append(Room(x, y, width, height, type))
            return Room(x, y, width, height, type)

        tree_node.left_tree.dungeon_size = cls.generate_room(tree_node.left_tree, n + 1)
        tree_node.right_tree.dungeon_size = cls.generate_room(tree_node.right_tree, n + 1)
        return tree_node.left_tree.dungeon_size

    @classmethod
    def generate_road(cls, tree_node, n):
        size1 = None
        size2 = None
        if n == cls.max_node:
            rooms_copy = cls.rooms[:]
            size1 = r.choice(rooms_copy)
            rooms_copy.remove(size1)
            size2 = r.choice(rooms_copy)
        else:
            size1 = tree_node.left_tree.dungeon_size
            size2 = tree_node.right_tree.dungeon_size
        x1 = cls.get_center_X(size1)
        y1 = cls.get_center_Y(size1)
        x2 = cls.get_center_X(size2)
        y2 = cls.get_center_Y(size2)
        type1 = None
        type2 = None
        if r.randint(0, 0) == 0:
            type1 = pygame.transform.scale(Road1, (max(x1, x2) - min(x1, x2), 10))
            type2 = pygame.transform.scale(Road1, (10, max(y1, y2) - min(y1, y2)))
        cls.roads.append(Road(min(x1, x2), y1, max(x1, x2), y1, type1))
        cls.roads.append(Road(x2, min(y1, y2), x2, max(y1, y2), type2))

        if n != cls.max_node:
            cls.generate_road(tree_node.left_tree, n + 1)
            cls.generate_road(tree_node.right_tree, n + 1)

    @classmethod
    def draw_dungeon(cls):
        for road in cls.roads:
            SCREEN.blit(road.type, (road.x, road.y))
        for room in cls.rooms:
            SCREEN.blit(room.type, (room.x, room.y))

# ==========================================================================================

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dungeon")

# ==========================================================================================

Room1 = pygame.image.load("sprites/black_square.png").convert_alpha()
Road1 = pygame.image.load("sprites/grey_square.png").convert_alpha()

# ==========================================================================================

def main():
    Dungeon.Make_dungeon((SCREEN_WIDTH, SCREEN_HEIGHT), 3)

    run = True
    while run:
        # reset
        SCREEN.fill((255, 255, 255))

        # event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    Dungeon.Make_dungeon((SCREEN_WIDTH, SCREEN_HEIGHT), 3)

        Dungeon.draw_dungeon()

        # update
        pygame.display.flip()


# ==========================================================================================

if __name__ == "__main__":
    main()
    pygame.quit()
    sys.exit()
