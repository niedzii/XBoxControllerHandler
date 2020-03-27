import pygame
import sys

from Platform import Platform

MAX_POSITIVE_VALUE = 0.99609375
MAX_NEGATIVE_VALUE = -0.99609375

LINUX = 0
WINDOWS = 2

if sys.platform.startswith("lin"):
    platform = Platform.LINUX
elif sys.platform.startswith("win"):
    platform = Platform.WINDOWS

A = 1000
B = 1
X = 2
Y = 3
LEFT_BUMP = 4
RIGHT_BUMP = 5
BACK = 6
START = 7
LEFT_STICK_X = 0
LEFT_STICK_Y = 1

if platform == Platform.LINUX:
    LEFT_STICK_BTN = 9
    RIGHT_STICK_BTN = 10

    # axes
    RIGHT_STICK_X = 3
    RIGHT_STICK_Y = 4
    LEFT_TRIGGER = 2
    RIGHT_TRIGGER = 5

elif platform == Platform.WINDOWS:
    # buttons
    LEFT_STICK_BTN = 8
    RIGHT_STICK_BTN = 9

    # axes
    RIGHT_STICK_X = 4
    RIGHT_STICK_Y = 3
    TRIGGERS = 2


class Controller:
    id_num = 0

    def __init__(self, dead_zone=0.15):
        """
        Initializes a controller. IDs for controllers begin at 0 and increment by 1
        each time a controller is initialized.

        Args:
            dead_zone: The size of dead zone for the analog sticks (default 0.15)
        """

        self.joystick = pygame.joystick.Joystick(Controller.id_num)
        self.joystick.init()
        self.dead_zone = dead_zone

        # Linux and Mac triggers behave funny. See get_triggers().
        self.left_trigger_used = False
        self.right_trigger_used = False

        Controller.id_num += 1

    def dead_zone_adjustment(self, value):
        """
        Analog sticks likely wont ever return to exact center when released. Without
        a dead zone, it is likely that a small axis value will cause game objects
        to drift. This adjustment allows for a full range of input while still
        allowing a little bit of 'play' in the dead zone.

        Returns:
            Axis value outside of the dead zone remapped proportionally onto the
            -1.0 <= value <= 1.0 range.
        """

        if value > self.dead_zone:
            return (value - self.dead_zone) / (1 - self.dead_zone)
        elif value < -self.dead_zone:
            return (value + self.dead_zone) / (1 - self.dead_zone)
        else:
            return 0

    def get_left_stick(self):
        """
        Gets the state of the left analog stick.

        Returns:
            The x & y axes as a tuple such that

            -1 <= x <= 1 && -1 <= y <= 1

            Negative values are left and up.
            Positive values are right and down.
        """

        left_stick_x = self.dead_zone_adjustment(self.joystick.get_axis(LEFT_STICK_X))
        left_stick_y = self.dead_zone_adjustment(self.joystick.get_axis(LEFT_STICK_Y))

        return left_stick_x, left_stick_y

    def get_right_stick(self):
        """
        Gets the state of the right analog stick.

        Returns:
            The x & y axes as a tuple such that

            -1 <= x <= 1 && -1 <= y <= 1

            Negative values are left and up.
            Positive values are right and down.
        """

        right_stick_x = self.dead_zone_adjustment(self.joystick.get_axis(RIGHT_STICK_X))
        right_stick_y = self.dead_zone_adjustment(self.joystick.get_axis(RIGHT_STICK_Y))

        return right_stick_x, right_stick_y

    def get_triggers(self):
        """
        Gets the state of the triggers.

        On Windows, both triggers work additively to return a single axis, whereas
        triggers on Linux and Mac function as independent axes. In this interface,
        triggers will behave additively for all platforms so that pygame controllers
        will work consistently on each platform.

        Also note that the value returned is on Windows is multiplied by -1 so that
        negative is to the left and positive to the right to be consistent with
        stick axes.

        On Linux and Mac, trigger axes return 0 if they haven't been used yet. Once
        used, an unpulled trigger returns 1 and pulled returns -1. The trigger_used
        booleans keep the math correct for triggers prior to use.

        Returns:
            A float in the range -1.0 <= value <= 1.0 where -1.0 represents full
            left and 1.0 represents full right. If the triggers are pulled
            simultaneously, then the sum of the trigger pulls is returned.
        """

        trigger_axis = 0.0

        if platform == Platform.LINUX:
            left = self.joystick.get_axis(LEFT_TRIGGER)
            right = self.joystick.get_axis(RIGHT_TRIGGER)

            if left != 0:
                self.left_trigger_used = True
            if right != 0:
                self.right_trigger_used = True

            if not self.left_trigger_used:
                left = -1
            if not self.right_trigger_used:
                right = -1

            trigger_axis = (-1 * left + right) / 2

        elif platform == Platform.WINDOWS:
            trigger_axis = -1 * self.joystick.get_axis(TRIGGERS)

        return smoothOutput(trigger_axis)


def smoothOutput(input):
    if input == MAX_POSITIVE_VALUE:
        return 1

    if input == MAX_NEGATIVE_VALUE:
        return -1

    return round(input, 2)
