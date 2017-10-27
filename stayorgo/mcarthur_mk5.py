from math import exp, log, ceil


##################################################################
# For a valid calculation the following input conditions must be met
# humidity: between 0 and 100%
# temperature: between 0 and 45 degrees C
# wind_speed: between 0 and 70 km/hr
# drought_factor: between 0 and 10
#
def calc_mcarthur_forest(temperature, humidity, wind_speed, drought=10):
    # assume max drought factor as default

    # from http://www.firebreak.com.au/forest-5.html
    # k = 2*(Math.exp((.987*Math.log(h+0.001))-.45-(.0345*c)+(.0338*b)+(.0234*d)));//forest mk5
    mcarthur = ceil(2 * exp((0.987 * log(drought + 0.001))
                            - 0.45 - (0.0345 * humidity) + (0.0338 * temperature) + (0.0234 * wind_speed)))

    return mcarthur


def calc_mcarthur_grass():
    mcarthur = 'Not implemented yet...'
    return mcarthur


def calc_fdr(fdi, scope='forest'):
    fdr = ''
    if scope == 'forest':
        if fdi < 12:
            fdr = 'Low-Moderate'
        elif fdi >= 12 and fdi < 25:
            fdr = 'High'
        elif fdi >= 25 and fdi < 50:
            fdr = 'Very High'
        elif fdi >= 50 and fdi < 75:
            fdr = 'Severe'
        elif fdi >= 75 and fdi < 100:
            fdr = 'Extreme'
        elif fdi >= 100:
            fdr = 'Code Red'
        else:
            fdr = 'NaN'

    if scope == 'grass':
        if fdi < 12:
            fdr = 'Low-Moderate'
        elif fdi >= 12 and fdi < 25:
            fdr = 'High'
        elif fdi >= 25 and fdi < 50:
            fdr = 'Very High'
        elif fdi >= 50 and fdi < 100:
            fdr = 'Severe'
        elif fdi >= 100 and fdi < 150:
            fdr = 'Extreme'
        elif fdi >= 150:
            fdr = 'Code Red'
        else:
            fdr = 'NaN'

    return fdr


if __name__ == '__main__':
    ffdi = calc_mcarthur_forest(40.0, 10.0, 10.0)
    print(ffdi, calc_fdr(ffdi))
