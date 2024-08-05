class BatteryMonitor:
    def __init__(self, reporter, language='en'):
        self.reporter = reporter
        self.language = language
        self.messages = {
            'en': {
                'low_temp': 'Temperature too low!',
                'high_temp': 'Temperature too high!',
                'low_temp_warning': 'Warning: Approaching low temperature limit',
                'high_temp_warning': 'Warning: Approaching high temperature limit',
                'low_soc': 'State of Charge too low!',
                'high_soc': 'State of Charge too high!',
                'low_soc_warning': 'Warning: Approaching discharge',
                'high_soc_warning': 'Warning: Approaching charge-peak',
                'high_charge_rate': 'Charge rate too high!',
                'high_charge_rate_warning': 'Warning: Approaching high charge rate',
            },
            'de': {
                'low_temp': 'Temperatur zu niedrig!',
                'high_temp': 'Temperatur zu hoch!',
                'low_temp_warning': 'Warnung: Annäherung an niedrige Temperaturgrenze',
                'high_temp_warning': 'Warnung: Annäherung an hohe Temperaturgrenze',
                'low_soc': 'Ladezustand zu niedrig!',
                'high_soc': 'Ladezustand zu hoch!',
                'low_soc_warning': 'Warnung: Annäherung an Entladung',
                'high_soc_warning': 'Warnung: Annäherung an Ladehöhepunkt',
                'high_charge_rate': 'Laderate zu hoch!',
                'high_charge_rate_warning': 'Warnung: Annäherung an hohe Laderate',
            }
        }

    def get_message(self, key):
        return self.messages[self.language][key]

    def report(self, condition, warning_condition, breach_msg, warning_msg):
        if condition:
            self.reporter(self.get_message(breach_msg))
            return False
        elif warning_condition:
            self.reporter(self.get_message(warning_msg))
        return True

    def check_temperature(self, temperature):
        return (
            self.report(temperature < 0, temperature < 0 + 2.25, 'low_temp', 'low_temp_warning') and
            self.report(temperature > 45, temperature > 45 - 2.25, 'high_temp', 'high_temp_warning')
        )

    def check_soc(self, soc):
        return (
            self.report(soc < 20, soc < 20 + 4, 'low_soc', 'low_soc_warning') and
            self.report(soc > 80, soc > 80 - 4, 'high_soc', 'high_soc_warning')
        )

    def check_charge_rate(self, charge_rate):
        return self.report(charge_rate > 0.8, charge_rate > 0.8 - 0.04, 'high_charge_rate', 'high_charge_rate_warning')

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
    monitor = BatteryMonitor(console_reporter, language='en')

    assert(monitor.battery_is_ok(25, 70, 0.7) is True)
    assert(monitor.battery_is_ok(50, 70, 0.7) is False)
    assert(monitor.battery_is_ok(25, 85, 0.7) is False)
    assert(monitor.battery_is_ok(25, 70, 0.9) is False)
    assert(monitor.battery_is_ok(-5, 15, 0.9) is False)

    monitor_de = BatteryMonitor(console_reporter, language='de')
    assert(monitor_de.battery_is_ok(25, 70, 0.7) is True)
    assert(monitor_de.battery_is_ok(50, 70, 0.7) is False)
    assert(monitor_de.battery_is_ok(25, 85, 0.7) is False)
    assert(monitor_de.battery_is_ok(25, 70, 0.9) is False)
    assert(monitor_de.battery_is_ok(-5, 15, 0.9) is False)

    print('All tests passed (maybe!)')
