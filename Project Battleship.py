"""
COMP.CS.100 Ohjelmointi 1 / Programming 1
Name: Zareen Rahman (zareen.rahman@tuni.fi)
Student Number: 151788983
"""
class FileReadError(Exception):
    pass

class ShipSunkError(Exception):
    pass
class Ship:
    def __init__(self, ship_type, coordinates):
        """
        Initialize a Ship object.

        Parameters:
        - ship_type (str): Type of the ship.
        - coordinates (list): List of tuples representing the coordinates of the ship.
        """
        self.ship_type = ship_type
        self.coordinates = coordinates
        self.hits = [False] * len(coordinates)

    def is_sunk(self):
        """
        Check if the ship is sunk (all coordinates are hit).

        Returns:
        - bool: True if the ship is sunk, False otherwise.
        """
        return all(self.hits)

    def take_hit(self, coordinate):
        """
        Mark the specified coordinate as hit.

        Parameters:
        - coordinate (tuple): Tuple representing the coordinate to mark as hit.
        """
        index = self.coordinates.index(coordinate)
        self.hits[index] = True

class BattleshipGame:
    def __init__(self):
        """
        Initialize a BattleshipGame object.
        """
        self.ships = []
        self.board = [[' ' for _ in range(10)] for _ in range(10)]

    def print_board(self):
        """
        Print the current state of the game board.
        """
        print("\n  A B C D E F G H I J")
        for i in range(10):
            print(i, end=' ')
            for j in range(10):
                print(self.board[i][j], end=' ')
            print(i)
        print("  A B C D E F G H I J\n")

    def is_valid_input(self, user_input):
        """
        Check if the user input is a valid coordinate.

        Parameters:
        - user_input (str): User input representing a coordinate.

        Returns:
        - bool: True if the input is valid, False otherwise.
        """
        if len(user_input) != 2 or not user_input[0].isalpha() or not user_input[1].isdigit():
            print("Invalid command!")
            return False

        col = ord(user_input[0].upper()) - ord('A')
        row = int(user_input[1]) - 1  # Subtract 1 to convert to 0-based index

        if not (col < 10) or not (row < 10):
            print("Invalid coordinates!")
            return False

        return True
    def load_ships_from_file(self, file_name):
        """
        Load ships from a file and initialize the game.

        Parameters:
        - file_name (str): Name of the file containing ship data.

        Raises:
        - FileReadError: If there is an error reading the file or processing ship coordinates.
        """
        try:
            with open(file_name, 'r') as file:
                for line in file:
                    ship_data = line.strip().split(';')
                    ship_type = ship_data[0]
                    coordinates = []

                    for coord in ship_data[1:]:
                        if len(coord) < 2 or not coord[0].isalpha() or not coord[1:].isdigit():
                            raise FileReadError(
                                f"Error in ship coordinates! Invalid coordinate format: {coord}")

                        col = ord(coord[0].upper()) - ord('A')
                        row = int(coord[1:])

                        # Check if coordinates are within the valid range
                        if not (0 <= col < 10) or not (0 <= row < 10):
                            raise FileReadError(
                                f"Error in ship coordinates!")# Coordinates must be between A0 and J9. Invalid coordinates: {coord}

                        coordinates.append((row, col))

                    ship = Ship(ship_type, coordinates)

                    # Check for overlapping ships
                    for existing_ship in self.ships:
                        if any(coord in existing_ship.coordinates for coord in ship.coordinates):
                            raise FileReadError(
                                "There are overlapping ships in the input file!")

                    self.ships.append(ship)
        except FileNotFoundError:
            raise FileReadError("File can not be read!")
        except FileReadError as e:
            raise e  # Re-raise the specific error
        except Exception:
            raise FileReadError("Error in ship coordinates!")
    def process_user_input(self, user_input):
        """
        Process the user's input for shooting at a location.

        Parameters:
        - user_input (str): User input representing a coordinate.

        Returns:
        - bool: True if the board should be printed, False otherwise.
        """
        if not self.is_valid_input(user_input):
            return False

        col = ord(user_input[0].upper()) - ord('A')
        row = int(user_input[1])

        if self.board[row][col] in ['*', 'X']:
            print("Location has already been shot at!")
            return False

        should_print_board = self.check_and_update_ships(row, col)

    def check_and_update_ships(self, row, col):
        """
        Check if a ship is hit and update the game board.

        Parameters:
        - row (int): Row index of the target coordinate.
        - col (int): Column index of the target coordinate.

        Returns:
        - bool: True if the board should be printed, False otherwise.
        """
        hit_ship = None
        for ship in self.ships:
            if (row, col) in ship.coordinates:
                hit_ship = ship
                break

        if hit_ship:
            hit_ship.take_hit((row, col))
            self.board[row][col] = 'X'

            if hit_ship.is_sunk():
                ship_type_initial = hit_ship.ship_type[0].upper()
                print(f"You sank a {hit_ship.ship_type}!")

                for coordinate in hit_ship.coordinates:
                    r, c = coordinate
                    self.board[r][c] = ship_type_initial

                if all(s.is_sunk() for s in self.ships):
                    self.print_board()
                    raise ShipSunkError("Congratulations! You sank all enemy ships")

            return True

        self.board[row][col] = '*'
        return True

    def play_game(self):
        """
        Main game loop for playing Battleship.
        """
        while True:
            self.print_board()
            user_input = input("Enter place to shoot (q to quit): ")

            if user_input.lower() == 'q':
                print("Aborting game!")
                break

            should_print_board = self.process_user_input(user_input)

            if should_print_board:
                self.print_board()
def main():
    game = BattleshipGame()
    file_name = input("Enter file name: ")

    try:
        game.load_ships_from_file(file_name)
    except FileReadError as e:
        print(f"{e}")
        return
    try:
        game.play_game()
    except ShipSunkError:
        print("Congratulations! You sank all enemy ships.")

if __name__ == "__main__":
    main()