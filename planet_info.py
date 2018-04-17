
class Neptune:

    name = 'Neptune'
    pixel_scale = 0.033
    rotation_time = 16.11 #hours
    rotational_velocity = 2.86
    polar_radius = 24341
    equatorial_radius = 24764

class Uranus:

    name = 'Uranus'
    rotational_velocity = 2.59
    polar_radius = 24973
    equatorial_radius = 25559

class NeptuneH(Neptune):

    def __init__(self):
        self.band = 'Neptune_H'
        self.vmin = 0
        self.vmax = 800

class NeptuneKs(Neptune):

    def __init__(self):
        self.band = 'Neptune_Ks'
        self.vmin = 0
        self.vmax = 1000

class UranusH(Uranus):

    def __init__(self):
        self.band = 'Uranus_H'
        self.vmin = 0
        self.vmax = 1900

class UranusKs(Uranus):

    def __init__(self):
        self.band = 'Uranus_Ks'
        self.vmin = 0
        self.vmax = 300

