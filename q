from pyorbital.orbital import Orbital
from datetime import datetime
orb = Orbital("Suomi NPP")
now = datetime.utcnow()
orb.get_position(now)
orb.get_lonlatalt(now)
