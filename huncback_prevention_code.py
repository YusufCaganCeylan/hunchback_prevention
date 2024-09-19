from machine import SoftI2C, Pin, PWM
import deneyap
import time
from mpu6050 import MPU6050

# I2C settings
i2c = SoftI2C(scl=Pin(deneyap.SCL), sda=Pin(deneyap.SDA))  # Deneyap Board pin configuration
sensor_bottom = MPU6050(i2c, addr=0x68)  # Bottom sensor address
sensor_top = MPU6050(i2c, addr=0x69)    # Top sensor address

# Servo motor pin configuration
tilt_servo = PWM(Pin(deneyap.D0), freq=50)
pull_servo = PWM(Pin(deneyap.D1), freq=50)

def write_angle(servo, angle):
    duty = int((angle / 180) * 1023 + 26)  # Convert 0-180 degrees to PWM signal
    servo.duty(duty)

def tilt():
    for pos in range(90, -1, -1):
        write_angle(tilt_servo, pos)
        time.sleep(0.01)
    for zero in range(91):
        write_angle(tilt_servo, zero)
        time.sleep(0.01)

def pull():
    write_angle(pull_servo, 90)

def setup():
    print("Initializing MPU6050 sensors...")
    if not sensor_bottom.testConnection():  # Test bottom sensor connection
        raise OSError("Bottom sensor connection failed.")
    if not sensor_top.testConnection():  # Test top sensor connection
        raise OSError("Top sensor connection failed.")

def detect_posture(sensor_data):
    # sensor_data: [bottom_acc_x, bottom_acc_y, bottom_acc_z, bottom_gyro_x, bottom_gyro_y, bottom_gyro_z, top_acc_x, top_acc_y, top_acc_z, top_gyro_x, top_gyro_y, top_gyro_z]

    # Decision Trees for posture detection
    # Tree 0
    if sensor_data[8] <= 6986.00:
        if sensor_data[4] <= -395.50:
            if sensor_data[2] <= 10552.00:
                if sensor_data[6] <= 14044.00:
                    return 1.0
                else:
                    return 0.0
            else:
                return 1.0
        else:
            if sensor_data[0] <= 12310.00:
                return 1.0
            else:
                return 0.0
    else:
        return 1.0

    # Tree 1
    if sensor_data[2] <= 10522.00:
        return 0.0
    else:
        if sensor_data[8] <= 7548.00:
            return 0.0
        else:
            return 1.0

    # Tree 2
    if sensor_data[2] <= 10456.00:
        return 0.0
    else:
        if sensor_data[8] <= 7548.00:
            return 0.0
        else:
            return 1.0

    # Tree 3
    if sensor_data[2] <= 10494.00:
        return 0.0
    else:
        if sensor_data[7] <= -2246.00:
            if sensor_data[6] <= 14466.00:
                return 1.0
            else:
                return 0.0
        else:
            if sensor_data[8] <= 7754.00:
                return 0.0
            else:
                return 1.0

    # Tree 4
    if sensor_data[6] <= 13918.00:
        return 1.0
    else:
        if sensor_data[1] <= -3122.00:
            return 0.0
        else:
            if sensor_data[4] <= float('inf'):
                return 1.0
            else:
                return 0.0

    # Tree 5
    if sensor_data[1] <= -2998.00:
        return 0.0
    else:
        if sensor_data[7] <= -2178.00:
            if sensor_data[11] <= 73.50:
                if sensor_data[6] <= 14630.00:
                    return 1.0
                else:
                    return 0.0
            else:
                return 0.0
        else:
            return 1.0

    # Tree 6
    if sensor_data[2] <= 10494.00:
        return 0.0
    else:
        if sensor_data[6] <= 13956.00:
            return 1.0
        else:
            return 0.0

    # Tree 7
    if sensor_data[0] <= 12516.00:
        if sensor_data[8] <= 7548.00:
            return 0.0
        else:
            return 1.0
    else:
        return 0.0

    # Tree 8
    if sensor_data[8] <= 6968.00:
        if sensor_data[2] <= 10522.00:
            return 0.0
        else:
            return 1.0
    else:
        return 1.0

    # Tree 9
    if sensor_data[9] <= 598.50:
        if sensor_data[6] <= 14340.00:
            return 1.0
        else:
            return 0.0
    else:
        return 1.0

    # Tree 10
    if sensor_data[6] <= 14302.00:
        return 1.0
    else:
        return 0.0

    # Tree 11
    if sensor_data[8] <= 7548.00:
        if sensor_data[1] <= -3170.00:
            return 0.0
        else:
            return 1.0
    else:
        return 1.0

    # Tree 12
    if sensor_data[2] <= 10456.00:
        if sensor_data[8] <= 7548.00:
            if sensor_data[1] <= -2614.00:
                return 0.0
            else:
                return 1.0
        else:
            return 1.0
    else:
        return 1.0

    # Tree 13
    if sensor_data[8] <= 6968.00:
        if sensor_data[1] <= -3358.00:
            if sensor_data[4] <= -71.00:
                if sensor_data[3] <= -179.50:
                    if sensor_data[0] <= 11948.00:
                        return 1.0
                    else:
                        return 0.0
                else:
                    return 0.0
            else:
                return 0.0
        else:
            return 1.0
    else:
        return 1.0

    # Tree 14
    if sensor_data[7] <= -2178.00:
        if sensor_data[10] <= -466.50:
            if sensor_data[7] <= -2808.00:
                if sensor_data[6] <= 14350.00:
                    return 1.0
                else:
                    return 0.0
            else:
                return 0.0
        else:
            if sensor_data[8] <= 6450.00:
                return 0.0
            else:
                return 1.0
    else:
        if sensor_data[0] <= 12516.00:
            return 1.0
        else:
            if sensor_data[8] <= 7640.00:
                return 0.0
            else:
                return 1.0

    # Tree 15
    if sensor_data[2] <= 10456.00:
        return 0.0
    else:
        if sensor_data[6] <= 14440.00:
            return 1.0
        else:
            return 0.0

    # Tree 16
    if sensor_data[1] <= -3236.00:
        return 0.0
    else:
        if sensor_data[8] <= 7584.00:
            return 0.0
        else:
            return 1.0

    # Tree 17
    if sensor_data[6] <= 13956.00:
        return 1.0
    else:
        if sensor_data[3] <= -472.00:
            if sensor_data[0] <= 11822.00:
                return 1.0
            else:
                return 0.0
        else:
            if sensor_data[2] <= 10522.00:
                return 0.0
            else:
                return 1.0

    # Tree 18
    if sensor_data[1] <= -3358.00:
        return 0.0
    else:
        if sensor_data[8] <= 7548.00:
            return 0.0
        else:
            return 1.0

    # Tree 19
    if sensor_data[8] <= 7548.00:
        if sensor_data[5] <= 1128.00:
            if sensor_data[4] <= -204.00:
                if sensor_data[2] <= 10554.00:
                    return 0.0
                else:
                    return 1.0
            else:
                if sensor_data[5] <= -327.00:
                    if sensor_data[0] <= 12528.00:
                        return 1.0
                    else:
                        return 0.0
                else:
                    if sensor_data[0] <= 12632.00:
                        return 1.0
                    else:
                        return 0.0
        else:
            return 0.0
    else:
        return 1.0

    # Tree 20
    if sensor_data[1] <= -3170.00:
        return 0.0
    else:
        return 1.0

    # Tree 21
    if sensor_data[1] <= -3170.00:
        return 0.0
    else:
        if sensor_data[10] <= 70.50:
            if sensor_data[6] <= 13956.00:
                return 1.0
            else:
                return 0.0
        else:
            if sensor_data[6] <= 14186.00:
                return 1.0
            else:
                return 0.0

    # Tree 22
    if sensor_data[9] <= -611.50:
        if sensor_data[10] <= -339.00:
            if sensor_data[8] <= 6992.00:
                return 0.0
            else:
                return 1.0
        else:
            return 0.0
    else:
        if sensor_data[8] <= 6860.00:
            if sensor_data[0] <= 12200.00:
                return 1.0
            else:
                if sensor_data[10] <= 19.50:
                    return 0.0
                else:
                    if sensor_data[10] <= 67.50:
                        return 1.0
                    else:
                        return 0.0
        else:
            return 1.0

    # Tree 23
    if sensor_data[1] <= -3310.00:
        if sensor_data[6] <= 13956.00:
            return 1.0
        else:
            if sensor_data[4] <= 1562.00:
                if sensor_data[1] <= -2504.00:
                    return 0.0
                else:
                    return 1.0
            else:
                return 0.0
    else:
        return 1.0

    # Tree 24
    if sensor_data[6] <= 13956.00:
        return 1.0
    else:
        if sensor_data[2] <= 10494.00:
            return 0.0
        else:
            return 1.0

    # Tree 25
    if sensor_data[0] <= 12200.00:
        return 1.0
    else:
        return 0.0

    # Tree 26
    if sensor_data[0] <= 12078.00:
        if sensor_data[6] <= 14440.00:
            return 1.0
        else:
            return 0.0
    else:
        return 0.0

    # Tree 27
    if sensor_data[1] <= -3170.00:
        if sensor_data[6] <= 13892.00:
            return 1.0
        else:
            return 0.0
    else:
        return 1.0

    # Tree 28
    if sensor_data[0] <= 12200.00:
        return 1.0
    else:
        if sensor_data[6] <= 13956.00:
            return 1.0
        else:
            return 0.0

    # Tree 29
    if sensor_data[7] <= -2178.00:
        if sensor_data[10] <= -476.00:
            return 0.0
        else:
            if sensor_data[6] <= 14598.00:
                return 1.0
            else:
                return 0.0
    else:
        if sensor_data[0] <= 12038.00:
            return 1.0
        else:
            if sensor_data[8] <= 7766.00:
                return 0.0
            else:
                return 1.0

    # Tree 30
    if sensor_data[2] <= 10522.00:
        if sensor_data[9] <= -496.00:
            if sensor_data[7] <= -2302.00:
                if sensor_data[10] <= 306.00:
                    if sensor_data[6] <= 14224.00:
                        return 1.0
                    else:
                        return 0.0
                else:
                    return 0.0
            else:
                return 0.0
        else:
            if sensor_data[8] <= 6886.00:
                return 0.0
            else:
                return 1.0
    else:
        return 1.0

    # Tree 31
    if sensor_data[1] <= -3170.00:
        return 0.0
    else:
        return 1.0

    # Tree 32
    if sensor_data[10] <= -263.00:
        if sensor_data[3] <= 218.00:
            if sensor_data[1] <= -3358.00:
                return 0.0
            else:
                return 1.0
        else:
            if sensor_data[6] <= 14378.00:
                return 1.0
            else:
                return 0.0
    else:
        if sensor_data[9] <= -481.00:
            if sensor_data[7] <= -2498.00:
                if sensor_data[10] <= 83.50:
                    return 0.0
                else:
                    return 1.0
            else:
                return 0.0
        else:
            if sensor_data[8] <= 6968.00:
                return 0.0
            else:
                return 1.0

    # Tree 33
    if sensor_data[0] <= 12200.00:
        if sensor_data[6] <= 13918.00:
            return 1.0
        else:
            return 0.0
    else:
        return 0.0

    # Tree 34
    if sensor_data[2] <= 10494.00:
        return 0.0
    else:
        if sensor_data[8] <= 6968.00:
            return 0.0
        else:
            return 1.0

    # Tree 35
    if sensor_data[0] <= 12200.00:
        if sensor_data[8] <= 7548.00:
            return 0.0
        else:
            return 1.0
    else:
        return 0.0

    # Tree 36
    if sensor_data[0] <= 12200.00:
        if sensor_data[7] <= -2226.00:
            if sensor_data[8] <= 6590.00:
                return 0.0
            else:
                return 1.0
        else:
            if sensor_data[7] <= 62.00:
                if sensor_data[9] <= -478.00:
                    return 0.0
                else:
                    if sensor_data[6] <= 14376.00:
                        return 1.0
                    else:
                        return 0.0
            else:
                return 1.0
    else:
        return 0.0

    # Tree 37
    if sensor_data[7] <= -2038.00:
        if sensor_data[2] <= 10494.00:
            return 0.0
        else:
            if sensor_data[6] <= 13956.00:
                return 1.0
            else:
                return 0.0
    else:
        if sensor_data[6] <= 14480.00:
            return 1.0
        else:
            return 0.0

    # Tree 38
    if sensor_data[1] <= -3310.00:
        if sensor_data[8] <= 7548.00:
            return 0.0
        else:
            return 1.0
    else:
        return 1.0

    # Tree 39
    if sensor_data[4] <= -387.00:
        if sensor_data[0] <= 11996.00:
            return 1.0
        else:
            return 0.0
    else:
        return 1.0

    # Tree 40
    if sensor_data[1] <= -3170.00:
        if sensor_data[9] <= -685.50:
            if sensor_data[9] <= -431.50:
                if sensor_data[6] <= 13866.00:
                    return 1.0
                else:
                    if sensor_data[0] <= 11986.00:
                        return 1.0
                    else:
                        return 0.0
            else:
                return 0.0
        else:
            return 1.0
    else:
        return 1.0

    # Tree 41
    if sensor_data[8] <= 7612.00:
        if sensor_data[5] <= -1016.50:
            if sensor_data[8] <= 8036.00:
                return 0.0
            else:
                return 1.0
        else:
            if sensor_data[5] <= -118.50:
                if sensor_data[5] <= -151.50:
                    if sensor_data[4] <= -309.50:
                        if sensor_data[1] <= -3274.00:
                            return 0.0
                        else:
                            return 1.0
                    else:
                        if sensor_data[4] <= 6.50:
                            if sensor_data[1] <= -3842.00:
                                return 0.0
                            else:
                                return 1.0
                        else:
                            if sensor_data[0] <= 12552.00:
                                return 1.0
                            else:
                                return 0.0
                else:
                    return 1.0
            else:
                if sensor_data[2] <= 10342.00:
                    return 0.0
                else:
                    return 1.0
    else:
        return 1.0

    # Tree 42
    if sensor_data[8] <= 7566.00:
        if sensor_data[2] <= 10456.00:
            if sensor_data[0] <= 11930.00:
                return 1.0
            else:
                return 0.0
        else:
            return 1.0
    else:
        return 1.0

    # Tree 43
    if sensor_data[8] <= 7548.00:
        if sensor_data[6] <= 13550.00:
            if sensor_data[1] <= -3170.00:
                return 0.0
            else:
                return 1.0
        else:
            return 0.0
    else:
        return 1.0

    # Tree 44
    if sensor_data[8] <= 7548.00:
        if sensor_data[0] <= 12200.00:
            return 1.0
        else:
            return 0.0
    else:
        return 1.0

    # Tree 45
    if sensor_data[8] <= 6968.00:
        return 0.0
    else:
        return 1.0

    # Tree 46
    if sensor_data[7] <= -2194.00:
        if sensor_data[10] <= -805.00:
            return 0.0
        else:
            if sensor_data[7] <= -2952.00:
                return 1.0
            else:
                if sensor_data[8] <= 6356.00:
                    return 0.0
                else:
                    return 1.0
    else:
        if sensor_data[6] <= 13842.00:
            return 1.0
        else:
            return 0.0

    # Tree 47
    if sensor_data[0] <= 12200.00:
        if sensor_data[6] <= 13918.00:
            return 1.0
        else:
            return 0.0
    else:
        return 0.0

    # Tree 48
    if sensor_data[1] <= -3170.00:
        return 0.0
    else:
        if sensor_data[10] <= -263.00:
            if sensor_data[10] <= -678.00:
                return 0.0
            else:
                if sensor_data[8] <= 7174.00:
                    return 0.0
                else:
                    return 1.0
        else:
            if sensor_data[8] <= 6968.00:
                return 0.0
            else:
                return 1.0

    # Tree 49
    if sensor_data[0] <= 12420.00:
        if sensor_data[6] <= 14376.00:
            if sensor_data[0] <= 13506.00:
                return 1.0
            else:
                return 0.0
        else:
            return 0.0
    else:
        return 0.0

    # Tree 50
    if sensor_data[8] <= 6986.00:
        if sensor_data[0] <= 11996.00:
            return 1.0
        else:
            return 0.0
    else:
        return 1.0

    # Tree 51
    if sensor_data[8] <= 6968.00:
        if sensor_data[5] <= -777.50:
            if sensor_data[8] <= 7264.00:
                return 0.0
            else:
                return 1.0
        else:
            if sensor_data[3] <= -287.50:
                if sensor_data[1] <= -2968.00:
                    return 0.0
                else:
                    return 1.0
            else:
                if sensor_data[0] <= 12542.00:
                    return 1.0
                else:
                    return 0.0
    else:
        return 1.0

    # Tree 52
    if sensor_data[2] <= 10494.00:
        if sensor_data[7] <= -2194.00:
            if sensor_data[7] <= -3174.00:
                if sensor_data[10] <= -732.00:
                    return 0.0
                else:
                    return 1.0
            else:
                if sensor_data[8] <= 6608.00:
                    return 0.0
                else:
                    return 1.0
        else:
            if sensor_data[10] <= -320.50:
                if sensor_data[5] <= -373.50:
                    if sensor_data[5] <= -416.50:
                        return 0.0
                    else:
                        return 1.0
                else:
                    return 0.0
            else:
                if sensor_data[10] <= -274.00:
                    return 1.0
                else:
                    return 0.0
    else:
        return 1.0

    # Tree 53
    if sensor_data[2] <= 10582.00:
        if sensor_data[6] <= 13956.00:
            return 1.0
        else:
            return 0.0
    else:
        return 1.0

    # Tree 54
    if sensor_data[8] <= 6958.00:
        if sensor_data[2] <= 10494.00:
            return 0.0
        else:
            return 1.0
    else:
        return 1.0

    # Tree 55
    if sensor_data[8] <= 6968.00:
        if sensor_data[2] <= 10494.00:
            return 0.0
        else:
            return 1.0
    else:
        return 1.0

    # Tree 56
    if sensor_data[0] <= 11996.00:
        return 1.0
    else:
        if sensor_data[7] <= -2226.00:
            if sensor_data[7] <= -3542.00:
                return 0.0
            else:
                if sensor_data[10] <= 77.50:
                    if sensor_data[10] <= 398.50:
                        if sensor_data[8] <= 6308.00:
                            return 0.0
                        else:
                            return 1.0
                    else:
                        if sensor_data[7] <= -2556.00:
                            return 1.0
                        else:
                            return 0.0
                else:
                    if sensor_data[6] <= 14214.00:
                        return 1.0
                    else:
                        return 0.0
        else:
            if sensor_data[10] <= 54.50:
                if sensor_data[6] <= 14538.00:
                    return 1.0
                else:
                    return 0.0
            else:
                if sensor_data[7] <= -624.00:
                    return 0.0
                else:
                    return 1.0

    # Tree 57
    if sensor_data[1] <= -3170.00:
        return 0.0
    else:
        if sensor_data[8] <= 7584.00:
            return 0.0
        else:
            return 1.0

    # Tree 58
    if sensor_data[0] <= 12200.00:
        if sensor_data[8] <= 6836.00:
            return 0.0
        else:
            return 1.0
    else:
        return 0.0

    # Tree 59
    if sensor_data[1] <= -3170.00:
        if sensor_data[10] <= 73.50:
            if sensor_data[6] <= 14574.00:
                return 1.0
            else:
                return 0.0
        else:
            if sensor_data[7] <= -2030.00:
                if sensor_data[6] <= 14498.00:
                    return 1.0
                else:
                    return 0.0
            else:
                if sensor_data[5] <= 36.00:
                    return 0.0
                else:
                    return 1.0
    else:
        return 1.0

    # Tree 60
    if sensor_data[6] <= 13956.00:
        return 1.0
    else:
        if sensor_data[1] <= -3236.00:
            return 0.0
        else:
            return 1.0
           # Tree 61
    if sensor_data[0] <= 12516.00:
        if sensor_data[8] <= 7548.00:
            return 0.0
        else:
            if sensor_data[1] <= -3692.00:
                return 0.0
            else:
                return 1.0
    else:
        if sensor_data[2] <= float('inf'):
            return 0.0
        else:
            return 1.0

    # Tree 62
    if sensor_data[7] <= -2178.00:
        if sensor_data[1] <= -3122.00:
            return 0.0
        else:
            if sensor_data[6] <= 14340.00:
                return 1.0
            else:
                return 0.0
    else:
        if sensor_data[8] <= 7780.00:
            return 0.0
        else:
            return 1.0

    # Tree 63
    if sensor_data[2] <= 10596.00:
        return 0.0
    else:
        if sensor_data[8] <= 6968.00:
            return 0.0
        else:
            return 1.0

    # Tree 64
    if sensor_data[2] <= 10522.00:
        if sensor_data[6] <= 14340.00:
            return 1.0
        else:
            return 0.0
    else:
        return 1.0

    # Tree 65
    if sensor_data[6] <= 13956.00:
        return 1.0
    else:
        if sensor_data[0] <= 12200.00:
            return 1.0
        else:
            return 0.0

    # Tree 66
    if sensor_data[2] <= 10418.00:
        return 0.0
    else:
        if sensor_data[6] <= 14504.00:
            return 1.0
        else:
            return 0.0

    # Tree 67
    if sensor_data[2] <= 10494.00:
        return 0.0
    else:
        if sensor_data[7] <= -2038.00:
            if sensor_data[11] <= 77.50:
                if sensor_data[10] <= 1091.50:
                    if sensor_data[9] <= -466.50:
                        return 0.0
                    else:
                        if sensor_data[6] <= 14682.00:
                            return 1.0
                        else:
                            return 0.0
                else:
                    return 1.0
            else:
                if sensor_data[8] <= 6762.00:
                    return 0.0
                else:
                    return 1.0
        else:
            if sensor_data[10] <= 154.00:
                if sensor_data[7] <= -1968.00:
                    if sensor_data[9] <= -212.50:
                        return 0.0
                    else:
                        if sensor_data[6] <= 14714.00:
                            return 1.0
                        else:
                            return 0.0
                else:
                    return 0.0
            else:
                if sensor_data[7] <= 978.00:
                    if sensor_data[7] <= -1470.00:
                        if sensor_data[6] <= 14448.00:
                            return 1.0
                        else:
                            return 0.0
                    else:
                        return 0.0
                else:
                    if sensor_data[6] <= 13714.00:
                        return 1.0
                    else:
                        return 0.0

    # Tree 68
    if sensor_data[6] <= 14574.00:
        return 1.0
    else:
        if sensor_data[2] <= 10494.00:
            if sensor_data[11] <= 117.00:
                return 0.0
            else:
                if sensor_data[1] <= -3414.00:
                    return 0.0
                else:
                    return 1.0
        else:
            if sensor_data[3] <= float('inf'):
                return 1.0
            else:
                return 0.0

    # Tree 69
    if sensor_data[6] <= 14440.00:
        return 1.0
    else:
        if sensor_data[8] <= float('inf'):
            return 0.0
        else:
            if sensor_data[2] <= 10418.00:
                return 0.0
            else:
                return 1.0

    # Tree 70
    if sensor_data[6] <= 14440.00:
        return 1.0
    else:
        if sensor_data[0] <= 12200.00:
            return 1.0
        else:
            return 0.0

    # Tree 71
    if sensor_data[6] <= 13956.00:
        return 1.0
    else:
        if sensor_data[2] <= 10494.00:
            return 0.0
        else:
            return 1.0

    # Tree 72
    if sensor_data[1] <= -3366.00:
        return 0.0
    else:
        if sensor_data[7] <= -2178.00:
            if sensor_data[10] <= 14340.00:
                return 1.0
            else:
                return 0.0
        else:
            if sensor_data[11] <= 1708.00:
                if sensor_data[12] <= 50.50:
                    if sensor_data[6] <= 13842.00:
                        return 1.0
                    else:
                        return 0.0
                else:
                    if sensor_data[8] <= 7232.00:
                        return 0.0
                    else:
                        return 1.0
            else:
                return 1.0

    # Tree 73
    if sensor_data[8] <= 7548.00:
        if sensor_data[0] <= 12078.00:
            return 1.0
        else:
            return 0.0
    else:
        return 1.0

    # Tree 74
    if sensor_data[2] <= 10494.00:
        return 0.0
    else:
        if sensor_data[8] <= 7548.00:
            return 0.0
        else:
            return 1.0

    # Tree 75
    if sensor_data[0] <= 12516.00:
        if sensor_data[10] <= -522.50:
            if sensor_data[10] <= -752.00:
                return 0.0
            else:
                if sensor_data[8] <= 6864.00:
                    return 0.0
                else:
                    return 1.0
        else:
            if sensor_data[6] <= 14612.00:
                return 1.0
            else:
                return 0.0
    else:
        return 0.0

    # Tree 76
    if sensor_data[6] <= 13956.00:
        return 1.0
    else:
        if sensor_data[0] <= 12200.00:
            return 1.0
        else:
            return 0.0

    # Tree 77
    if sensor_data[8] <= 7584.00:
        if sensor_data[1] <= -3170.00:
            return 0.0
        else:
            return 1.0
    else:
        return 1.0

    # Tree 78
    if sensor_data[8] <= 7548.00:
        return 0.0
    else:
        if sensor_data[7] <= float('inf'):
            return 1.0
        else:
            if sensor_data[9] <= -1588.50:
                return 0.0
            else:
                if sensor_data[12] <= 105.50:
                    if sensor_data[2] <= 10494.00:
                        return 0.0
                    else:
                        return 1.0
                else:
                    if sensor_data[2] <= 9908.00:
                        return 0.0
                    else:
                        return 1.0

    # Tree 79
    if sensor_data[6] <= 14340.00:
        return 1.0
    else:
        if sensor_data[9] <= -1339.00:
            return 0.0
        else:
            if sensor_data[9] <= -632.00:
                return 1.0
            else:
                if sensor_data[1] <= -3342.00:
                    return 0.0
                else:
                    return 1.0

    # Tree 80
    if sensor_data[8] <= 7548.00:
        if sensor_data[10] <= 893.50:
            if sensor_data[12] <= 346.50:
                if sensor_data[1] <= -3390.00:
                    return 0.0
                else:
                    return 1.0
            else:
                if sensor_data[1] <= -3912.00:
                    return 0.0
                else:
                    return 1.0
        else:
            return 0.0
    else:
        return 1.0

    # Tree 81
    if sensor_data[0] <= 12200.00:
        if sensor_data[7] <= -2226.00:
            if sensor_data[6] <= 14408.00:
                if sensor_data[7] <= float('inf'):
                    return 1.0
                else:
                    if sensor_data[0] <= 13870.00:
                        return 1.0
                    else:
                        return 0.0
            else:
                return 0.0
        else:
            if sensor_data[8] <= 7186.00:
                return 0.0
            else:
                return 1.0
    else:
        return 0.0

    # Tree 82
    if sensor_data[6] <= 13956.00:
        return 1.0
    else:
        if sensor_data[1] <= -3170.00:
            return 0.0
        else:
            return 1.0

    # Tree 83
    if sensor_data[6] <= 13956.00:
        return 1.0
    else:
        if sensor_data[9] <= -1339.00:
            return 0.0
        else:
            if sensor_data[0] <= 12354.00:
                return 1.0
            else:
                return 0.0

    # Tree 84
    if sensor_data[0] <= 12200.00:
        if sensor_data[7] <= -2210.00:
            if sensor_data[6] <= 14340.00:
                return 1.0
            else:
                return 0.0
        else:
            if sensor_data[10] <= -505.00:
                return 0.0
            else:
                if sensor_data[6] <= 14376.00:
                    return 1.0
                else:
                    return 0.0
    else:
        return 0.0

    # Tree 85
    if sensor_data[2] <= 10522.00:
        return 0.0
    else:
        if sensor_data[8] <= 7548.00:
            return 0.0
        else:
            return 1.0

    # Tree 86
    if sensor_data[2] <= 10494.00:
        return 0.0
    else:
        if sensor_data[0] <= float('inf'):
            return 1.0
        else:
            if sensor_data[8] <= 7548.00:
                return 0.0
            else:
                return 1.0

    # Tree 87
    if sensor_data[6] <= 13892.00:
        return 1.0
    else:
        if sensor_data[10] <= 660.50:
            if sensor_data[1] <= -3358.00:
                return 0.0
            else:
                return 1.0
        else:
            if sensor_data[0] <= 12864.00:
                return 1.0
            else:
                return 0.0

    # Tree 88
    if sensor_data[2] <= 10494.00:
        if sensor_data[10] <= -345.50:
            if sensor_data[6] <= 13854.00:
                return 1.0
            else:
                return 0.0
        else:
            if sensor_data[7] <= -2250.00:
                if sensor_data[6] <= 14662.00:
                    return 1.0
                else:
                    return 0.0
            else:
                if sensor_data[9] <= 546.50:
                    if sensor_data[12] <= 43.50:
                        if sensor_data[7] <= 694.00:
                            if sensor_data[8] <= 7154.00:
                                return 0.0
                            else:
                                return 1.0
                        else:
                            if sensor_data[6] <= 13336.00:
                                return 1.0
                            else:
                                return 0.0
                    else:
                        return 0.0
                else:
                    return 1.0
    else:
        return 1.0

    # Tree 89
    if sensor_data[10] <= -700.00:
        return 0.0
    else:
        if sensor_data[8] <= 6968.00:
            if sensor_data[12] <= -774.00:
                return 0.0
            else:
                if sensor_data[11] <= 711.50:
                    if sensor_data[2] <= 10544.00:
                        return 0.0
                    else:
                        return 1.0
                else:
                    if sensor_data[12] <= -606.00:
                        return 1.0
                    else:
                        if sensor_data[0] <= 12560.00:
                            return 1.0
                        else:
                            return 0.0
        else:
            return 1.0

    # Tree 90
    if sensor_data[6] <= 13956.00:
        return 1.0
    else:
        if sensor_data[2] <= 10494.00:
            if sensor_data[0] <= 11944.00:
                return 1.0
            else:
                return 0.0
        else:
            if sensor_data[10] <= float('inf'):
                return 1.0
            else:
                return 0.0

    # Tree 91
    if sensor_data[1] <= -3170.00:
        return 0.0
    else:
        if sensor_data[11] <= float('inf'):
            if sensor_data[6] <= 13956.00:
                return 1.0
            else:
                return 0.0
        else:
            return 1.0

    # Tree 92
    if sensor_data[1] <= -3366.00:
        if sensor_data[7] <= -2178.00:
            if sensor_data[9] <= -435.50:
                return 0.0
            else:
                if sensor_data[6] <= 14624.00:
                    return 1.0
                else:
                    return 0.0
        else:
            if sensor_data[8] <= 7186.00:
                return 0.0
            else:
                return 1.0
    else:
        return 1.0

    # Tree 93
    if sensor_data[9] <= -272.50:
        if sensor_data[8] <= 6976.00:
            return 0.0
        else:
            return 1.0
    else:
        if sensor_data[0] <= 12516.00:
            if sensor_data[6] <= 13956.00:
                if sensor_data[10] <= 2359.50:
                    if sensor_data[1] <= -4048.00:
                        return 0.0
                    else:
                        return 1.0
                else:
                    return 1.0
            else:
                return 0.0
        else:
            if sensor_data[10] <= float('inf'):
                return 0.0
            else:
                return 1.0

    # Tree 94
    if sensor_data[8] <= 7548.00:
        return 0.0
    else:
        if sensor_data[1] <= -3040.00:
            if sensor_data[1] <= float('inf'):
                return 0.0
            else:
                return 1.0
        else:
            if sensor_data[9] <= -251.00:
                if sensor_data[9] <= -263.00:
                    return 1.0
                else:
                    return 0.0
            else:
                return 1.0

    # Tree 95
    if sensor_data[6] <= 13918.00:
        return 1.0
    else:
        if sensor_data[2] <= 10522.00:
            if sensor_data[2] <= 10818.00:
                return 0.0
            else:
                return 1.0
        else:
            if sensor_data[2] <= float('inf'):
                return 1.0
            else:
                return 0.0

    # Tree 96
    if sensor_data[8] <= 6968.00:
        if sensor_data[9] <= float('inf'):
            return 0.0
        else:
            if sensor_data[1] <= -2998.00:
                return 0.0
            else:
                return 1.0
    else:
        return 1.0

    # Tree 97
    if sensor_data[6] <= 13918.00:
        return 1.0
    else:
        if sensor_data[11] <= -1016.50:
            if sensor_data[1] <= -2762.00:
                if sensor_data[11] <= -581.50:
                    return 0.0
                else:
                    return 1.0
            else:
                return 0.0
        else:
            if sensor_data[1] <= -3366.00:
                return 0.0
            else:
                return 1.0

    # Tree 98
    if sensor_data[0] <= 12200.00:
        return 1.0
    else:
        if sensor_data[11] <= 118.50:
            if sensor_data[11] <= -310.00:
                if sensor_data[7] <= -2814.00:
                    if sensor_data[7] <= -3114.00:
                        return 0.0
                    else:
                        return 1.0
                else:
                    return 0.0
            else:
                if sensor_data[8] <= 7548.00:
                    return 0.0
                else:
                    return 1.0
        else:
            if sensor_data[8] <= 7228.00:
                if sensor_data[9] <= -12.00:
                    return 0.0
                else:
                    if sensor_data[6] <= 14512.00:
                        return 1.0
                    else:
                        return 0.0
            else:
                if sensor_data[10] <= float('inf'):
                    return 1.0
                else:
                    return 0.0

    # Tree 99
    if sensor_data[0] <= 12200.00:
        if sensor_data[1] <= float('inf'):
            return 1.0
        else:
            if sensor_data[6] <= 13956.00:
                return 1.0
            else:
                return 0.0
    else:
        return 0.0

    return 0.0


def loop():
    while True:
        try:
            bottom_acc_x, bottom_acc_y, bottom_acc_z, bottom_gyro_x, bottom_gyro_y, bottom_gyro_z = sensor_bottom.get_motion6()
            top_acc_x, top_acc_y, top_acc_z, top_gyro_x, top_gyro_y, top_gyro_z = sensor_top.get_motion6()
            sensor_data = [bottom_acc_x, bottom_acc_y, bottom_acc_z, bottom_gyro_x, bottom_gyro_y, bottom_gyro_z,
                           top_acc_x, top_acc_y, top_acc_z, top_gyro_x, top_gyro_y, top_gyro_z]

            posture = detect_posture(sensor_data)
            print("Detected Posture:", posture)

            if posture == 1.0:
                tilt()
                pull()
            else:
                write_angle(pull_servo, 0)

            time.sleep(0.1)
        except OSError as e:
            print("I2C connection error: ", e)
            time.sleep(1)  


setup()
loop()