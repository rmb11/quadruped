from machine import Pin, PWM

class Servo:
    """Represents a servo motor controlled via PWM.

    Attributes:
        __servo_pwm_freq (int): PWM frequency used for the servo (default 50Hz).
        __min_u16_duty (int): Minimum 16-bit duty cycle value for the servo.
        __max_u16_duty (int): Maximum 16-bit duty cycle value for the servo.
        min_angle (int): Minimum angle the servo can rotate to (default 0).
        max_angle (int): Maximum angle the servo can rotate to (default 180).
        current_angle (float): Current angle of the servo.
    """
    __servo_pwm_freq = 50
    __min_u16_duty = 1640 - 2 # offset for correction
    __max_u16_duty = 7864 - 0  # offset for correction
    min_angle = 0
    max_angle = 180
    current_angle = 0.001


    def __init__(self, pin):
        """Initialises the servo instance and sets up PWM.

        Args:
            pin (int): The GPIO pin number where the servo is connected"""
        self.__initialise(pin)


    def update_settings(self, servo_pwm_freq, min_u16_duty, max_u16_duty, min_angle, max_angle, pin):
        """Updates servo's settings and reinitialises it.

        Args:
            servo_pwm_freq (int): New PWM frequency for the servo.
            min_u16_duty (int): New minimum 16-bit duty cycle value.
            max_u16_duty (int): New maximum 16-bit duty cycle value.
            min_angle (int): New minimum angle for the servo.
            max_angle (int): New maximum angle for the servo.
            pin (int): The GPIO pin number where the servo is connected.
        """
        self.__servo_pwm_freq = servo_pwm_freq
        self.__min_u16_duty = min_u16_duty
        self.__max_u16_duty = max_u16_duty
        self.min_angle = min_angle
        self.max_angle = max_angle
        self.__initialise(pin)


    def move(self, angle):
        """Moves the servo to the specified angle.

        If the angle matches the current angle, no action is taken.

        Args:
            angle (int): Desired angle to move the servo to in degrees.

        Raises:
            ValueError: If the angle is outside the valid range.
        """
        angle = round(angle, 2)
        if angle == self.current_angle:
            return
        self.current_angle = angle
        duty_u16 = self.__angle_to_u16_duty(angle)
        self.__motor.duty_u16(duty_u16)

    def __angle_to_u16_duty(self, angle):
        """Converts angle in degrees to 16-bit PWM duty cycle value.

        Conversion is based on the servo's configured minimum and maximum duty cycle values and the angle range.

        Args:
            angle (int): Angle in degrees to convert.

        Returns:
            int: 16-bit duty cycle value corresponding to the angle.
        """
        return int((angle - self.min_angle) * self.__angle_conversion_factor) + self.__min_u16_duty


    def __initialise(self, pin):
        """Initialises or reinitialises the servo with the given pin.

        Sets up the PWM frequency and calculates the angle-to-duty-cycle conversion factor.

        Args:
            pin (int): The GPIO pin number where the servo is connected.
        """
        self.current_angle = -0.001
        self.__angle_conversion_factor = (self.__max_u16_duty - self.__min_u16_duty) / (self.max_angle - self.min_angle)
        self.__motor = PWM(Pin(pin))
        self.__motor.freq(self.__servo_pwm_freq)