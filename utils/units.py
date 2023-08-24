import logging
logging.basicConfig(level=logging.DEBUG)

def convert_charge(value, from_unit, to_unit):
    units = {'C': 1, 'mC': 1e-3, 'uC': 1e-6, 'kC': 1e3}
    converted_value = value * units[from_unit] / units[to_unit]
    print(f"Converting charge: {value} {from_unit} to {to_unit} = {converted_value}")
    return converted_value

def convert_capacitance(value, from_unit, to_unit):
    units = {'F': 1, 'mF': 1e-3, 'uF': 1e-6, 'nF': 1e-9, 'pF': 1e-12}
    logging.debug(f"Converting capacitance: {value} {from_unit} to {to_unit}")

    if from_unit not in units:
        logging.error(f"Invalid from_unit: {from_unit}")
        raise ValueError(f"Invalid from_unit: {from_unit}")

    if to_unit not in units:
        logging.error(f"Invalid to_unit: {to_unit}")
        raise ValueError(f"Invalid to_unit: {to_unit}")

    converted_value = value * units[from_unit] / units[to_unit]
    logging.debug(f"Converted value: {converted_value}")
    return converted_value


def convert_voltage(value, from_unit, to_unit):
    units = {'V': 1, 'mV': 1e-3, 'uV': 1e-6, 'kV': 1e3}
    converted_value = value * units[from_unit] / units[to_unit]
    print(f"Converting voltage: {value} {from_unit} to {to_unit} = {converted_value}")
    return converted_value

def convert_current(value, from_unit, to_unit):
    units = {'A': 1, 'mA': 1e-3, 'uA': 1e-6, 'kA': 1e3}
    converted_value = value * units[from_unit] / units[to_unit]
    print(f"Converting current: {value} {from_unit} to {to_unit} = {converted_value}")
    return converted_value

def convert_energy(value, from_unit, to_unit):
    units = {'J': 1, 'mJ': 1e-3, 'uJ': 1e-6, 'kJ': 1e3}
    converted_value = value * units[from_unit] / units[to_unit]
    print(f"Converting energy: {value} {from_unit} to {to_unit} = {converted_value}")
    return converted_value

def convert_resistance(value, from_unit, to_unit):
    units = {'Ohm': 1, 'mOhm': 1e-3, 'uOhm': 1e-6, 'kOhm': 1e3}
    converted_value = value * units[from_unit] / units[to_unit]
    print(f"Converting resistance: {value} {from_unit} to {to_unit} = {converted_value}")
    return converted_value

def convert_power(value, from_unit, to_unit):
    units = {'W': 1, 'mW': 1e-3, 'uW': 1e-6, 'kW': 1e3}
    converted_value = value * units[from_unit] / units[to_unit]
    print(f"Converting power: {value} {from_unit} to {to_unit} = {converted_value}")
    return converted_value

def convert_time(value, from_unit, to_unit):
    units = {'s': 1, 'ms': 1e-3, 'us': 1e-6, 'min': 60, 'h': 3600}
    converted_value = value * units[from_unit] / units[to_unit]
    print(f"Converting time: {value} {from_unit} to {to_unit} = {converted_value}")
    return converted_value

def convert_density(value, from_unit, to_unit):
    units = {'Wh/kg': 1, 'Wh/l': 1, 'mAh/g': 1e-3}
    converted_value = value * units[from_unit] / units[to_unit]
    print(f"Converting density: {value} {from_unit} to {to_unit} = {converted_value}")
    return converted_value

def convert_temperature(value, from_unit, to_unit):
    if from_unit == 'C' and to_unit == 'F':
        converted_value = (value * 9/5) + 32
    elif from_unit == 'F' and to_unit == 'C':
        converted_value = (value - 32) * 5/9
    else:
        converted_value = value  # No conversion needed if units are the same
    print(f"Converting temperature: {value} {from_unit} to {to_unit} = {converted_value}")
    return converted_value

def convert_energy_units(energy, from_unit, to_unit, weight, volume):
    if from_unit == "J" and to_unit == "Ah":
        return energy / 3600  # Conversion from Joules to Ah
    elif from_unit == "Ah":
        return energy / 3600 / weight  # Conversion for Ah
    elif from_unit == "mAh":
        return (energy / 3600) * 1000 / weight  # Conversion for mAh
    elif from_unit == "Wh/kg":
        return float(energy) * weight  # Conversion for Wh/kg
    elif from_unit == "Wh/g":
        return float(energy) * weight * 1000  # Conversion for Wh/g
    elif from_unit == "Wh/l":
        return float(energy) * volume  # Conversion for Wh/l
    elif from_unit == "kW/kg":
        return float(energy) * weight * 1000  # Conversion for kW/kg
    elif from_unit == "kW/l":
        return float(energy) * volume * 1000  # Conversion for kW/l
    else:
        raise ValueError("Invalid unit")
