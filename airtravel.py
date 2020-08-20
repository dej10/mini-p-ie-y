class Flight:

    def __init__(self, number, aircraft):

        """"
        Aircraft numbers in the format : AA000
        eg BA786
        """

        self.aircraft = None

        if not number[:2].isalpha():            # validation@ of the airplane number, certain conditions to be .
            raise ValueError("No airline code in '{}'".format(number))

        if not (number[2:].isdigit() and int(number[2:]) <= 9999):
            raise ValueError("Invalid route number ' {}'".format(number))

        self._number = number
        self._aircraft = aircraft

        rows, seats = self._aircraft.seating_plan()
        self._seating = [None] + [{letter : None for letter in seats} for _ in rows]      #List comprenshions in a dictionary comp.

    def number(self):
        return self._number

    def airline(self):
        return self._number[:2]

    def aircraft_model(self):
        return self._aircraft.model()

    def _parse_seat(self, seat,):    #leading undescore before parse seat beacuse it is a leading implementation detail

        """
       to move passenger to another available seat
        """

        row_numbers, seat_letters = self._aircraft.seating_plan()

        letter = seat[-1]
        if letter not in seat_letters:
            raise ValueError("Invalid seat Letter {}".format(letter))

        row_text = seat[:-1]        #list silcing
        try:
            row = int(row_text)
        except ValueError:
            raise ValueError("Invalid seat row {}".format(row_text))

        if row not in row_numbers:
            raise ValueError("Invalid row number {}".format(row))

        return row, letter                                       #tuple

    def allocate_seat(self, seat, passenger):

        """
        :seat should be in the format eg. 10C, 12E, valid letters ABCDEFGHJK
        """
        row, letter = self._parse_seat(seat)

        if self._seating[row][letter] is not None:
            raise ValueError("Seat {} is already occupied ".format(seat))

        self._seating[row][letter] = passenger

    def relocate_passenger(self, from_seat, to_seat):

        from_row, from_letter = self._parse_seat(from_seat)
        if self._seating[from_row][from_letter] is None:
            raise ValueError("No passenger to relocate to Seat {}".format(from_seat))          # validation

        to_row, to_letter = self._parse_seat(to_seat)
        if self._seating[to_row][to_letter] is not None:                                        #validation
            raise ValueError("Seat {} already occupied ".format(to_seat))

        self._seating[to_row][to_letter] = self._seating[from_row][from_letter]
        self._seating[from_row][from_letter] = None

    # def seats_ava(self):
    #     return sum(sum(1 for s in row.values() if s is None)
    #                    for row is self._seating
    #                    if row is not None)

    def make_boarding_pass(self, card_printer):
        for passenger, seat in sorted(self._passenger_seats()):
            card_printer(passenger, self.number(),seat, self.aircraft_model())

    def _passenger_seats(self):
        """
        An iterable series of passenger seating allocations
        """
        row_numbers, seat_letters = self._aircraft.seating_plan()
        for row in row_numbers:
            for letter in seat_letters:
                passenger = self._seating[row][letter]
                if passenger is not None:
                    yield(passenger, "{}{}". format(row, letter))

class Aircraft:

    """
    inheritance used
    and then added to the aircraft class
    code dupilication has been resolved by put the copied code in the inheritance class

    """
    def num_seats(self):
        row,row_seats = self.seating_plan()
        return  len(row) * len(row_seats)


    def __init__(self, regi):
        self._regi = regi

    def regi(self):
        return self._regi


class AirBus8880(Aircraft):

    def model(self):
        return "Airbus 8880"

    def seating_plan(self):
         return range(1,23), "ABCDEF"


class Boieng737(Aircraft):

    def model(self):
        return "Boieng 737"

    def seating_plan(self):
         return range(1, 56), "ABCGEFGHJK"



def make_flights():
    g = Flight ("BA656", AirBus8880("G-EUPT"))
    g.allocate_seat("3B", "Zlat")

    f = Flight("DA354", Boieng737("F-GBHG"))
    f.allocate_seat("2B", "Ayodeji")

    return g,f

def console_card_printer(passenger, flight_num, seat, aircraft):
    output = "| Name {0}"     \
             "  Flight : {1}"  \
             "  Seat : {2}"     \
             "  Aircraft: {3}"   \
             " |".format(passenger, flight_num, seat,  aircraft)
    banner = '+' + '-' * (len(output)-2) + '+'
    border = '|' + ' ' * (len(output)-2) + '|'
    lines = [banner, border, output,border, banner]
    card  = '\n'.join(lines)
    print(card)
    print()
