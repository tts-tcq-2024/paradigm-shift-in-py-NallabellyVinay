class BatteryMonitor:
    def __init__(self, reporter, language='EN'):
        self.reporter = reporter
        self.language = language
        self.messages = {
            'EN': {
                'low_temp': 'Temperature too low!',
                'high_temp': 'Temperature too high!',
                'low_soc': 'State of Charge too low!',
                'high_soc': 'State of Charge too high!',
                'high_charge_rate': 'Charge rate too high!',
                'warn_discharge': 'Warning: Approaching discharge',
                'warn_charge_peak': 'Warning: Approaching charge-peak',
                'warn_low_temp': 'Warning: Temperature approaching lower limit',
                'warn_high_temp': 'Warning: Temperature approaching upper limit',
                'warn_high_charge_rate': 'Warning: Charge rate approaching upper limit'
            },
            'DE': {
                'low_temp': 'Temperatur zu niedrig!',
                'high_temp': 'Temperatur zu hoch!',
                'low_soc': 'Ladezustand zu niedrig!',
                'high_soc': 'Ladezustand zu hoch!',
                'high_charge_rate': 'Laderate zu hoch!',
                'warn_discharge': 'Warnung: Annäherung an Entladung',
                'warn_charge_peak': 'Warnung: Annäherung an Ladehöhepunkt',
                'warn_low_temp': 'Warnung: Temperatur nähert sich der unteren Grenze',
                'warn_high_temp': 'Warnung: Temperatur nähert sich der oberen Grenze',
                'warn_high_charge_rate': 'Warnung: Laderate nähert sich der oberen Grenze'
            }
        }

    def report(self, key):
        self.reporter(self.messages[self.language][key])

    def check_temperature(self, temperature):
        if temperature < 0:
            self.report('low_temp')
            return False
        elif temperature < 2.25:  # 5% of 45 is 2.25
            self.report('warn_low_temp')
        elif temperature > 45:
            self.report('high_temp')
            return False
        elif temperature > 42.75:  # 5% of 45 is 2.25
            self.report('warn_high_temp')
        return True

    def check_soc(self, soc):
        if soc < 20:
            self.report('low_soc')
            return False
        elif soc < 24:  # 5% of 80 is 4
            self.report('warn_discharge')
        elif soc > 80:
            self.report('high_soc')
            return False
        elif soc > 76:  # 5% of 80 is 4
            self.report('warn_charge_peak')
        return True

    def check_charge_rate(self, charge_rate):
        if charge_rate > 0.8:
            self.report('high_charge_rate')
            return False
        elif charge_rate > 0.76:  # 5% of 0.8 is 0.04
            self.report('warn_high_charge_rate')
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
    monitor = BatteryMonitor(console_reporter, language='EN')

    assert(monitor.battery_is_ok(25, 70, 0.7) is True)
    assert(monitor.battery_is_ok(50, 70, 0.7) is False)
    assert(monitor.battery_is_ok(25, 85, 0.7) is False)
    assert(monitor.battery_is_ok(25, 70, 0.9) is False)
    assert(monitor.battery_is_ok(-5, 15, 0.9) is False)

    print('All tests passed (maybe!)')

