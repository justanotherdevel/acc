

def control(speed=0, acceleration=0, car_in_front=200, gap=5, desired_speed=None, gas=0, brake=0):
    """Adaptive Cruise Control

       speed: Current car speed (m/s)
       acceleration: Current car acceleration (m/s^2)
       gas: last signal sent. Real number.
       brake: last signal sent. Real number.
       car_in_front: distance in meters to the car in front. (m)
       gap: maximum distance to the car in front (m)
    """
    a_d_min = -3
    a_d_max = 5
    K_p = 10
    K_d = .2

    control = 0
    accel_new = 0
    brake_new = 0

    # If the cruise control speed is not set, let's give the variable a sensible setting.
    if desired_speed is None:
        desired_speed = speed

    d_front_prev = 100
    t_safe = .5 # Safe time to apply brake, .5 s.

    brake = -acceleration
    gas = 0

    delta_distance = car_in_front - 2 * gap

    # Figure out what control signal should be sent to try to match the required speed
    if speed != desired_speed:
        control = K_p*(speed - desired_speed)

    # But override it if we are too close to the car in front.
    if delta_distance < 0:
        control = -K_p * delta_distance - K_d * car_in_front
        if control > a_d_max:
            control = a_d_max
        elif control < a_d_min:
            control = a_d_min

    if control > 0:
        accel_new = control
    if control < 0:
        brake_new = control

    brake = .5 * brake_new + .5 * brake
    gas = .5 * accel_new + .5 * gas

    return brake, gas
