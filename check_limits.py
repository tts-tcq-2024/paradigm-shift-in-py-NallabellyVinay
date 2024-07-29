class BatteryMonitor:
    def __init__(self, reporter):
        self.reporter = reporter
        self.temperature_warning_tolerance = 45 * 0.05
        self.soc_warning_tolerance = 80 * 0.05
        self.charge_rate_warning_tolerance = 0.8 * 0.05

    def check_temperature(self, temperature):
        if temperature < 0:
            self.reporter('Temperature too low!')
            return False
        if temperature >= 0 and temperature < 0 + self.temperature_warning_tolerance:
            self.reporter('Warning: Temperature approaching low limit')
        if temperature > 45:
            self.reporter('Temperature too high!')
            return False
        if temperature > 45 - self.temperature_warning_tolerance:
            self.reporter('Warning: Temperature approaching high limit')
        return True

    def check_soc(self, soc):
        if soc < 20:
            self.reporter('State of Charge too low!')
            return False
        if soc >= 20 and soc < 20 + self.soc_warning_tolerance:
            self.reporter('Warning: Approaching discharge')
        if soc > 80:
            self.reporter('State of Charge too high!')
            return False
        if soc > 80 - self.soc_warning_tolerance:
            self.reporter('Warning: Approaching charge-peak')
        return True

    def check_charge_rate(self, charge_rate):
        if charge_rate > 0.8:
            self.reporter('Charge rate too high!')
            return False
        if charge_rate > 0.8 - self.charge_rate_warning_tolerance:
            self.reporter('Warning: Charge rate approaching high limit')
        return True

    def battery_is_ok(self, temperature, soc, charge_rate):
        return (self.check_temperature(temperature) and
                self.check_soc(soc) and
                self.check_charge_rate(charge_rate))

def console_reporter(message):
    print(message)

def file_reporter(message):
    with open('battery_report.txt', 'a') as f:
        f.write(message + '\n')

# Testing
if __name__ == '__main__':
    monitor = BatteryMonitor(console_reporter)

    assert(monitor.battery_is_ok(25, 70, 0.7) is True)
    assert(monitor.battery_is_ok(50, 70, 0.7) is False)
    assert(monitor.battery_is_ok(25, 85, 0.7) is False)
    assert(monitor.battery_is_ok(25, 70, 0.9) is False)
    assert(monitor.battery_is_ok(-5, 15, 0.9) is False)

    monitor.battery_is_ok(2, 22, 0.75)  # This should trigger warnings

    print('All tests passed (maybe!)')
