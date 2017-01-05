#! /usr/bin/env python3

"""
    Copyright (C) 2016  B. Zolt'n Gorza
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
    
from enum import Enum, EnumMeta, unique
import math
import random


# constants
DEFAULT_RIGHT = "Right"
DEFAULT_WRONG = "" # "wrong"
MAX_GAME      = 1024


@unique
class Operations(Enum):
    """
    Enum of operations.
    """
    
    nothing  = " "
    add      = "+"
    subtract = "-"
    multiply = "*"
    division = "/"
    intdiv   = "\\"
    modulo   = "%"
    
    def __bool__(self):
        return not (self == Operations.nothing)
    
    def __str__(self):
        return self.value


def get_operations(without=[Operations.nothing]):
    """
    It returns all members of Operations without the operation(w)
    within the 'without' array.
    """
    out = []
    for o in Operations:
        if o not in without:
            out.append(o)
    return out


def write_out(stats, filename):
    """
    It writes the stats into a pure text file.
    """
    try:
        if (type(filename) is not str):
            raise TypeError
    except TypeError:
        print("Filename error -- given filename is not a string!")
        return
    f = open(filename + ".txt", 'w')
    f.write(stats)
    f.close()
    print("Game report is written into the {fname}.txt!".format(fname=filename))

class Expression:
    """
    It contains every informathions about.
    """
    
    # arguments
    _a          = None
    _b          = None
    #_c          = None # may will be used in the future

    # operation
    _operation  = Operations.nothing # it works as None

    # result of expression
    _result     = None

    # User's result
    _u_result   = None

    def __init__(self, a, b, o):
        """
        a: first argument
        b: second argument
        o: operation
        """
        self._a         = math.floor(a) if type(a) is float else a
        self._b         = math.floor(b) if type(b) is float else b
        self._operation = o
        self._result    = self._calc_result(a, b, o)

    def _calc_result(self, a, b, o):
        """
        It calculates the result of an expression.
        """
        if   o == Operations.add:
            return a +  b
        elif o == Operations.subtract:
            return a -  b
        elif o == Operations.multiply:
            return a *  b
        elif o == Operations.division:
            return a /  b
        elif o == Operations.intdiv:
            return a // b
        elif o == Operations.modulo:
            return a %  b
        else:
            return a

    def get_user_result(self, ur):
        """
        It gets the user's result.
        """
        self._u_result = ur if self._u_result is None \
                            else self._u_result

    def _validate_expression(self, o, a, b):
        """
        It makes some changes on the arguments, if necessary.
        It's also for make the expressions "easier" (or not-to-hard
                                                           at least)
        """
        # if it's a division, it makes sure that the first argument
        # is the greater one
        if ((#o == Operations.intdiv or
             #o == Operations.modulo or
             o == Operations.division) and
            (a < b)):
            a, b = b, a

        # these things make easier some expression (that may would
        # be too hard for lots)
        if ((o == Operations.division) or
            (o == Operations.intdiv) or
            (o == Operations.modulo)):
            b = b // 2
            if b == 0:
                b = 1
        elif o == Operations.multiply:
            b = b // 7
        return a, b

    @classmethod
    def make_expression(cls, operations=None, o=Operations.nothing):
        """
        It makes an expression with generated numbers.

        Parameters:
            operations: list of using operations
            o         : wanted operator (operations list
                                         will be ignored)
        """
        if not operations:
            operations = list(Operations)
        # initialize the arguments
        a = random.randint(0, 50)
        b = random.randint(1, 50)
        # if it's a real operation
        if not o:
            L = list(operations)
            o = L[random.randrange(1, len(L))]
        # if we didn't pass an operator
        else:
            pass
        a, b = cls._validate_expression(cls, o, a, b)
        
        return Expression(a, b, o)

    def _formatted_output(self):
        """
        It returns the formatted output of the expression
        without the result.
        """
        return ("{a:2d} {o:1} {b:2s} = ").format(
            a=self._a,
            b=str(self._b),
            o=str(self._operation)
        )

    def get_as_dict(self):
        """
        It returns the expression as a dictionary.
        This dictionary's keys:
            a : first argument
            b : second argument
            o : operator
            r0: expression's result
            r : user's result
        """
        return {
            'a' : self._a,
            'b' : self._b,
            'o' : str(self._operation),
            'r0': self._result,
            'r' : self._u_result
        }
    
    def __bool__(self):
        """
        It returns true when the user's and the expression's results
        are equal and results false, when the user's result is wrong,
        or one of both are missing (None).
        """
        if not(self._result == None and
               self._u_result == None):
            
            # if result isn't float
            if self._result is not float:
                return self._result == self._u_result
            # if result is float
            else:
                return "{:.2f}".format(
                            self._result
                        ) == "{:.2f}".format(
                                self._u_result
                            )
        else:
            return False
    
    def __str__(self):
        """
        It returns the expression as a 'formatted' string.
        
        If the user's result wasn't given, the returned form is for
        the game; if it's given, it returns for the report (with all
        of needed information, e.g.: user's result is right or not).
        """
        # in game form
        if self._u_result is None:
            return self._formatted_output()
        # statistic form
        else:
            return ("{a:2d} {o:1} {b:2s} = {r0:<10.2f} "
                    + "user's result: {r:<10.2f} "
                    + "{right}").format(
                a    =self._a,
                b    =str(self._b),
                o    =str(self._operation),
                r0   =float(self._result),
                r    =float(self._u_result),
                right=DEFAULT_RIGHT if self else DEFAULT_WRONG
            )

    def __float__(self):
        """
        It returns the expression's good result.
        """
        return self._result

    def __len__(self):
        """
        It returns the length of the expression (without the result)
        """
        return len(self._formatted_output())

class Statistics:
    """
    It saves the statistics.
    """

    # the number of games
    _num_of_games  = None

    # statistics of every user inputs as dictionary
    # {operator<str>: number_of_results<int>}
    _stats         = dict()

    # statistics of right user inputs as dictionary
    # {operator<str>: number_of_right_results<int>}
    _stats_right   = dict()

    # statistics of wrong user inputs as dictionary
    # {operator<str>: number_of_wrong_results<int>}
    _stats_wrong   = dict()

    # list of expressions (order: first to last)
    _expr          = list()

    # dictionary for nicer output {operator<str>: operators_name<str>}
    _operator_name = dict()

    def __init__(self, num_of_games, operators):
        """
        num_of_games: number of games
        operators   : a list of operations or the Operations enum itself
        """
        # if operators aren't valid, it exits
        if not (type(operators) is list or
                type(operators) is EnumMeta):
            raise TypeError
            import sys
            sys.exit()

        self._num_of_games = num_of_games

        # it defines the arrays of statistics via operators
        # (this is for the case, when we want to use own set of
        #  expressions)
        for o in operators:
            if o:
                self._stats[str(o)] = 0
                self._stats_right[str(o)] = 0
                self._stats_wrong[str(o)] = 0
                self._operator_name[str(o)] = o.name

    def _process_expression(self, expr):
        """
        It processes the expression to be added into statistics.
        """
        self._expr.append(expr)
        operator = expr.get_as_dict()['o']
        self._stats[operator] += 1
        if expr:
            self._stats_right[operator] += 1
        else:
            self._stats_wrong[operator] += 1
    
    def add_expression(self, expr):
        """
        Add an expression into the statistics.
        """
        if type(expr) is Expression:
            self._process_expression(expr)
        else:
            self._process_expression(Expression(-1,
                                                -1,
                                                Operations.nothing)
            )

    def _get_num_of_stats(self, stats):
        """
        Returns the number of some statistics.
        See:
            self._stats
            self._stats_right
            self._stats_wrong
        """
        num = 0
        for g in stats:
            num += stats[g]
        return num

    def _get_title(self, text, underchar="-"):
        """
        It returns a title with an underline.

        Parameters:
            text     : text of title
            underchar: character of underline
        """
        return "\n" + text + "\n" + underchar*len(text) + "\n\n"

    def _get_stats(self, title, stats):
        """
        It returns statistics with a title.
        
        Parameters:
            text : text of title
            stats: statistics

        See:
            self._stats
            self._stats_right
            self._stats_wrong
        """
        out = self._get_title(title)
        for o in sorted(self._operator_name,
                        key=self._operator_name.get):
            out += "    {:8s}: {:4d}\n".format(
                self._operator_name[o],
                stats[o]
            )
        return out

    def _get_expressions(self):
        """
        It returns all of the expressions.
        """
        out = ""
        for e in self._expr:
            out += str(e) + "\n"
        return out

    def get_as_dict(self):
        """
        It returns the statistics as a dictionary.

        This dictionary's keys:
            nog        : number of expressions
            stats      : dict of number of results per operator
            stats_right: dict of number of right results per operator
            stats_wrong: dict of number of wrong results per operator
            expr       : list of expressions
        """
        return {
            "nog"        : len(self._expr),
            "stats"      : self._stats,
            "stats_right": self._stats_right,
            "stats_wrong": self._stats_wrong,
            "expr"       : self._expr
        }

    def __bool__(self):
        """
        It returns true when all of it's fields have values.
        """
        return (self._stats_right and
                self._stats_wrong and
                self._expr and
                self._operator_name)

    def __str__(self):
        """
        It returns the statistics as a 'formatted' string.
        """
        return ("You had {nog} right result from {noe} expressions. " +
                "The game was {typ}.\n\n" +
                self._get_stats(
                    "Number of your results per operator:",
                    self._stats) +
                "\n" +
                self._get_stats(
                    "Number of your right results per operator:",
                    self._stats_right) +
                "\n" +
                self._get_stats(
                    "Number of your wrong results per operator:",
                    self._stats_wrong) +
                "\n" +
                self._get_title("Expressions of the game:") +
                self._get_expressions() +
                "").format(
                    nog=self._get_num_of_stats(self._stats_right),
                    noe=self._get_num_of_stats(self._stats),
                    typ="finite" if self._num_of_games else "infinite"
        )

class Game:
    """
    This is the class that manage everything.

    Contains:
        Input and validation
        Output
        Output for statistics, both console and file form
    """

    # number of games (if 0, it goes until
    # the user gives a wrong result or write 1000 good results)
    _numofgames = None

    # list of operations
    _operations = None

    # local instance of statistics
    _statistics = None

    def __init__(self, number_of_games=None, operations=None):
        """
        It initialize a new game.
        parameters:
            number_of_games<int>: (surprise, surprise) number of games
            o<Operations | list>: operations to be used
        """
        self._numofgames = number_of_games \
                           if number_of_games \
                           else self._get_number_of_games()
        self._operations = operations if operations \
                                      else get_operations()
        self._statistics = Statistics(self._numofgames, self._operations)

    def _get_number_of_games(self):
        """
        It asks, valid and returns the number of games.
        """
        try:
            nog = int(input("Please type the number of games: "))
            if nog not in range(0, MAX_GAME+1):
                raise ValueError
        except ValueError:
            print("Number of games has to be an integer between " +
                  "0 (infinite) and {}!".format(MAX_GAME))
            nog = self._get_number_of_games()
        finally:
            return nog

    def _get_user_input(self, expr_length=0, was_false=False):
        """
        It process the user input, if it was given. Otherwise it ask
        for an input. If user's input cannot be converted
        as a float, it return None.
        """
        user_input = input((" " * expr_length) if was_false \
                                                   else "")
        try:
            user_input = float(user_input.replace(",", "."))
        except ValueError:
            user_input = self._get_user_input(expr_length, True)
        finally:
            return user_input

    def _new_turn(self, nog):
        """
        Next turn of a game.
        """
        e = Expression.make_expression(self._operations)
        s = "{:4s}: {:s}".format(str(nog), str(e))
        print(s, end="")
        ui = self._get_user_input(len(s), False)
        e.get_user_result(ui)
        self._statistics.add_expression(e)
        return bool(e)

    def _game_engine(self, num_of_game):
        """
        It makes the game playable.
        
        The loop is in another function and it controls the input and
        the output.
        """
        is_right = self._new_turn(num_of_game)
        return is_right

    def _finite_game(self):
        """
        It is the loop of a finite game.
        """
        num = self._numofgames
        while num:
            self._game_engine(1 + self._numofgames - num)
            num -= 1

    def _infinite_game(self):
        """
        It is the loop of an infinite game.
        """
        number_of_game = 0
        last_is_right = True
        while last_is_right:
            number_of_game += 1
            last_is_right = self._game_engine(number_of_game)

    def start(self):
        """
        It starts a game. It also handle the things if it's over.
        """
        print()
        if self._numofgames == 0:
            self._infinite_game()
        else:
            self._finite_game()
        print("\nYour game is OVER.")
        input("Please press a key to continue")
        print("\n"*24)
        return str(self._statistics)
        

def hello():
    print("Hello!\n",
          "This is not a game.\nthis is THE game.",
          sep="\n",
          end="\n\n")


if __name__ == '__main__':
    hello()
    g = Game()
    stats = g.start()
    print(stats)
    write_out(stats, "report")
    input("Please press a key to exit")
