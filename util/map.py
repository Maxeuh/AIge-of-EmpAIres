from collections import defaultdict
from model.game_object import GameObject
from util.coordinate import Coordinate

"""
This file contains the Map class which is used to represent the map of the game and the methods associated with it.
It serves as the heart of the model-the representation of datas
"""
class Map():
    """
    The Map class is used to represent the map of the game. It contains the matrix of the map and the methods associated with it.
    """

    def __init__(self, size: int):
        """
        Create a map with a certain size.

        :param size: The size of the map.
        :type size: int
        """
        self.__size: int = size
        self.__matrix: defaultdict[Coordinate, GameObject] = defaultdict(lambda: None)

    def get_size(self) -> int:
        """
        Get the size of the map.

        :return: The size of the map.
        :rtype: int
        """
        return self.__size
    
    def check_placement(self, object: GameObject, coordinate: Coordinate) -> bool:
        """
        Check if an entity can be placed at a certain coordinate.

        :param object: The game object to be placed.
        :type object: GameObject
        :param coordinate: The coordinate where the object is to be placed.
        :type coordinate: Coordinate
        :return: True if the object can be placed, False otherwise.
        :rtype: bool
        """
        for x in range(object.get_size()):
            for y in range(object.get_size()):
                if coordinate is None or not (Coordinate(0, 0) <= coordinate and (coordinate + object.get_size() - 1) <= Coordinate(self.get_size() - 1, self.get_size() - 1)):
                    return False
                if self.get(Coordinate(coordinate.get_x() + x, coordinate.get_y() + y)) is not None:
                    return False
        return True

    def add(self, object: GameObject, coordinate: Coordinate):
        """
        Add an entity at a certain coordinate. It also claims other tiles depending on the size.

        :param object: The game object to be added.
        :type object: GameObject
        :param coordinate: The coordinate where the object is to be added.
        :type coordinate: Coordinate
        :raises ValueError: If the object cannot be placed at the given coordinate.
        """
        if not self.check_placement(object, coordinate):
            raise ValueError("Cannot place object at the given coordinate.")
        for x in range(object.get_size()):
            for y in range(object.get_size()):
                self.__matrix[Coordinate(coordinate.get_x() + x, coordinate.get_y() + y)] = object

    def __force_add(self, object: GameObject, coordinate: Coordinate):
        """
        Forcefully add an entity at a certain coordinate.

        :param object: The game object to be added.
        :type object: GameObject
        :param coordinate: The coordinate where the object is to be added.
        :type coordinate: Coordinate
        """
        self.__matrix[coordinate] = object

    def remove(self, coordinate: Coordinate) -> GameObject:
        """
        Remove the entity at a certain coordinate. It also removes other tiles depending on the size.

        :param coordinate: The coordinate from which the object is to be removed.
        :type coordinate: Coordinate
        :return: The removed game object.
        :rtype: GameObject
        :raises ValueError: If the coordinate is out of bounds or there is no entity at the given coordinate.
        """
        if not (Coordinate(0, 0) <= coordinate <= Coordinate(self.get_size(), self.get_size())):
            raise ValueError("Coordinate is out of bounds.")
        object: GameObject = self.__matrix[coordinate]
        if object is None:
            raise ValueError("No entity at the given coordinate.")
        for x in range(object.get_size()):
            for y in range(object.get_size()):
                self.__matrix[Coordinate(coordinate.get_x() + x, coordinate.get_y() + y)] = None
        return object
    
    def __force_remove(self, coordinate: Coordinate) -> GameObject:
        """
        Forcefully remove the entity at a certain coordinate.

        :param coordinate: The coordinate from which the object is to be removed.
        :type coordinate: Coordinate
        :return: The removed game object.
        :rtype: GameObject
        """
        object: GameObject = self.__matrix[coordinate]
        self.__matrix[coordinate] = None
        return object

    def move(self, object: GameObject, new_coordinate: Coordinate):
        """
        Move an entity to a new adjacent coordinate (8 surrounding coordinates).

        :param object: The game object to be moved.
        :type object: GameObject
        :param new_coordinate: The new coordinate where the object is to be moved.
        :type new_coordinate: Coordinate
        :raises ValueError: If the new coordinate is not adjacent or not available.
        """
        if not object.get_coordinate().is_adjacent(new_coordinate):
            raise ValueError("New coordinate is not adjacent to the entity's current coordinate.")
        if not self.check_placement(object, new_coordinate):
            raise ValueError("New coordinate is not available.")
        self.remove(object.get_coordinate())
        self.add(object, new_coordinate)

    def __force_move(self, object: GameObject, new_coordinate: Coordinate):
        """
        Forcefully move an entity to a new coordinate.

        :param object: The game object to be moved.
        :type object: GameObject
        :param new_coordinate: The new coordinate where the object is to be moved.
        :type new_coordinate: Coordinate
        """
        self.__force_remove(object.get_coordinate())
        self.__force_add(object, new_coordinate)
    
    def get(self, coordinate: Coordinate) -> GameObject:
        """
        Get the entity at a certain coordinate.

        :param coordinate: The coordinate from which the object is to be retrieved.
        :type coordinate: Coordinate
        :return: The game object at the given coordinate.
        :rtype: GameObject
        """
        return self.__matrix[coordinate]
    
    def get_map(self) -> defaultdict[Coordinate, GameObject]:
        """
        Get the map as a matrix.

        :return: The map as a matrix.
        :rtype: defaultdict[Coordinate, GameObject]
        """
        return self.__matrix
    
    def get_map_list(self) -> list[list[GameObject]]:
        """
        Get the map as a list of lists.

        :return: The map as a list of lists.
        :rtype: list[list[GameObject]]
        """
        return [[self.__matrix[Coordinate(i, j)] for j in range(self.get_size())] for i in range(self.get_size())]
    
    def get_from_to(self, from_coord: Coordinate, to_coord: Coordinate) -> 'Map':
        """
        Get the map from a certain coordinate to another as a new Map.

        :param from_coord: The starting coordinate.
        :type from_coord: Coordinate
        :param to_coord: The ending coordinate.
        :type to_coord: Coordinate
        :return: A new map from the starting coordinate to the ending coordinate.
        :rtype: Map
        """
        map = Map(self.get_size())
        for x in range(from_coord.get_x(), to_coord.get_x() + 1):
            for y in range(from_coord.get_y(), to_coord.get_y() + 1):
                obj = self.get(Coordinate(x, y))
                if obj is not None:
                    map.__force_add(obj, Coordinate(x, y))
        return map
    
    def get_map_from_to(self, from_coord: Coordinate, to_coord: Coordinate) -> defaultdict[Coordinate, GameObject]:
        """
        Get the map from a certain coordinate to another as a matrix.

        :param from_coord: The starting coordinate.
        :type from_coord: Coordinate
        :param to_coord: The ending coordinate.
        :type to_coord: Coordinate
        :return: A matrix from the starting coordinate to the ending coordinate.
        :rtype: defaultdict[Coordinate, GameObject]
        """
        result = defaultdict(lambda: None)
        for x in range(from_coord.get_x(), to_coord.get_x() + 1):
            for y in range(from_coord.get_y(), to_coord.get_y() + 1):
                obj = self.get(Coordinate(x, y))
                if obj is not None:
                    result[Coordinate(x, y)] = obj
        return result
    
    def get_map_list_from_to(self, from_coord: Coordinate, to_coord: Coordinate) -> list[list[GameObject]]:
        """
        Get the map as a list of lists from a certain coordinate to another.

        :param from_coord: The starting coordinate.
        :type from_coord: Coordinate
        :param to_coord: The ending coordinate.
        :type to_coord: Coordinate
        :return: A list of lists from the starting coordinate to the ending coordinate.
        :rtype: list[list[GameObject]]
        """
        size = self.get_size()
        result = [[None for _ in range(size)] for _ in range(size)]
        for x in range(from_coord.get_x(), to_coord.get_x() + 1):
            for y in range(from_coord.get_y(), to_coord.get_y() + 1):
                result[x][y] = self.get(Coordinate(x, y))
        return result
    
    def __repr__(self):
        """
        Get the string representation of the map for testing purposes.

        :return: The string representation of the map.
        :rtype: str
        """
        return f"smatrix({repr(self.get_map())})"
    
    def __str__(self) -> str:
        """
        Get the matrix of the map with table-like borders.

        :return: The matrix of the map as a string.
        :rtype: str
        """
        horizontal_line = lambda length: "┌" + "┬".join(["─" * 3] * length) + "┐"
        middle_line = lambda length: "├" + "┼".join(["─" * 3] * length) + "┤"
        bottom_line = lambda length: "└" + "┴".join(["─" * 3] * length) + "┘"
        
        rows = [horizontal_line(self.get_size())]
        for x in range(self.get_size()):
            row = []
            for y in range(self.get_size()):
                object = self.get(Coordinate(x, y))
                row.append(f" {object.get_letter() if object is not None else ' '} ")
            rows.append("│" + "│".join(row) + "│")
            if x < self.get_size() - 1:
                rows.append(middle_line(self.get_size()))
        rows.append(bottom_line(self.get_size()))
        return "\n".join(rows)