import re
from datetime import datetime, timezone
from math import pi, pow
from sgp4.ext import days2mdhms, jday
from sgp4.earth_gravity import wgs84

INT_RE = re.compile(r'[+-]?\d*')
FLOAT_RE = re.compile(r'[+-]?\d*(\.\d*)?')

LINE1 = '1 NNNNNC NNNNNAAA NNNNN.NNNNNNNN +.NNNNNNNN +NNNNN-N +NNNNN-N N NNNNN'
LINE2 = '2 NNNNN NNN.NNNN NNN.NNNN NNNNNNN NNN.NNNN NNN.NNNN NN.NNNNNNNNNNNNNN'

error_message = '''Invalid TLE error. The official format
for line {} followed by the line you provided:
{}
{}'''

class TLE:

    def __init__(self, line1, line2):
        self._line1 = line1
        self._line2 = line2

        line = line1.rstrip()

       # deg2rad = pi / 180.0;  # 0.0174532925199433
       # xpdotp = 1440.0 / (2.0 * pi);  # 229.1831180523293
       # tumin = wgs84.tumin

        try:
            assert line.startswith('1 ')
            self._satnum = int(line[2:7])
            assert line[8] == ' '
            two_digit_year = int(line[18:20])
            assert line[23] == '.'
            self.epochdays = float(line[20:32])
            assert line[32] == ' '
            assert line[34] == '.'
            #self.ndot = float(line[33:43])
            assert line[43] == ' '
            #self.nddot = float(line[44] + '.' + line[45:50])
            #nexp = int(line[50:52])
            assert line[52] == ' '
            #self.bstar = float(line[53] + '.' + line[54:59])
            #ibexp = int(line[59:61])
            assert line[61] == ' '
            assert line[63] == ' '
        except (AssertionError, IndexError, ValueError):
            raise ValueError(error_message.format(1, LINE1, line))

        line = line2.rstrip()
        try:
            assert line.startswith('2 ')
            self._satnum = int(line[2:7])  # TODO: check it matches line 1?
            assert line[7] == ' '
            assert line[11] == '.'
            #self.inclo = float(line[8:16])
            assert line[16] == ' '
            assert line[20] == '.'
            #self.nodeo = float(line[17:25])
            assert line[25] == ' '
            #self.ecco = float('0.' + line[26:33].replace(' ', '0'))
            assert line[33] == ' '
            assert line[37] == '.'
            #self.argpo = float(line[34:42])
            assert line[42] == ' '
            assert line[46] == '.'
            #self.mo = float(line[43:51])
            assert line[51] == ' '
            #self.no = float(line[52:63])
            #revnum = line[63:68]
        except (AssertionError, IndexError, ValueError):
            raise ValueError(error_message.format(2, LINE2, line))

        #  ---- find no, ndot, nddot ----
        #self.no   = self.no / xpdotp; #   rad/min
        #self.nddot= self.nddot * pow(10.0, nexp);
        #self.bstar= self.bstar * pow(10.0, ibexp);

        #  ---- convert to sgp4 units ----
        #self.a    = pow( self.no*tumin , (-2.0/3.0) );
        #self.ndot = self.ndot  / (xpdotp*1440.0);  #   ? * minperday
        #self.nddot= self.nddot / (xpdotp*1440.0*1440);

        #  ---- find standard orbital elements ----
        #self.inclo = self.inclo  * deg2rad;
        #self.nodeo = self.nodeo  * deg2rad;
        #self.argpo = self.argpo  * deg2rad;
        #self.mo    = self.mo     * deg2rad;

        #self.alta = self.a*(1.0 + self.ecco) - 1.0;
        #self.altp = self.a*(1.0 - self.ecco) - 1.0;

        if two_digit_year < 57:
            year = two_digit_year + 2000;
        else:
            year = two_digit_year + 1900;

        mon,day,hr,minute,sec = days2mdhms(year, self.epochdays);
        sec_whole, sec_fraction = divmod(sec, 1.0)

        self.epochyr = year
        self.jdsatepoch = jday(year,mon,day,hr,minute,sec);
        self._epoch = datetime(year, mon, day, hr, minute, int(sec_whole),
                                int(sec_fraction * 1000000.0 // 1.0), tzinfo=timezone.utc)

    @property
    def epoch(self):
        return self._epoch

    @property
    def satnum(self):
        return self._satnum

    @property
    def tle_line1(self):
        return self._line1

    @property
    def tle_line2(self):
        return self._line2

    @property
    def tle(self):
        return self.tle_line1, self.tle_line2

    def __repr__(self):
        return '({}, {})'.format(self.satnum, self.epoch.strftime('%Y/%m/%d %H:%M:%S'))
