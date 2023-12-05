from __future__ import annotations
from datetime import datetime

class Lightning:

    """
    A class that represents a lightningtime object.
    """

    def __init__(self, timestring:Timestring=None, static_bolt_color:tuple=None, static_zap_color:tuple=None, static_spark_color:tuple=None) -> None:
        self.timestring = timestring if timestring is not None else Timestring()
        self.static_bolt_color = (161, 0)
        self.static_zap_color = (50, 214)
        self.static_spark_color = (246, 133)
        self.static_bolt_color = static_bolt_color if static_bolt_color is not None else self.static_bolt_color
        self.static_zap_color = static_zap_color if static_zap_color is not None else self.static_zap_color
        self.static_spark_color = static_spark_color if static_spark_color is not None else self.static_spark_color
    
    @staticmethod
    def to_lightning(date:datetime) -> Lightning:

        """
        Converts a datetime object into a Lightning object.
        """
        
        total_sparks = (date.hour*60*60+date.minute*60+date.second)/(24*60*60)
        bolts = total_sparks*16
        zaps = (bolts-int(bolts))*16
        sparks = (zaps-int(zaps))*16
        charges = (sparks-int(sparks))*16
        return Lightning(Timestring(f"{hex(int(bolts))[2:]}~{hex(int(zaps))[2:]}~{hex(int(sparks))[2:]}|{hex(int(charges))[2:]}"))

    @staticmethod
    def from_lightning(lightning:Lightning, withseconds:bool=True) -> str:

        """
        Converts a Lightning object into a time string.
        """

        total_charges = (int(lightning.timestring.charges, 16)+int(lightning.timestring.sparks, 16)*16+int(lightning.timestring.zaps, 16)*16**2+int(lightning.timestring.bolts, 16)*16**3)/(16**4)
        hours = total_charges*24
        minutes = (hours-int(hours))*60
        seconds = (minutes-int(minutes))*60
        return f'{int(hours):02}:{int(minutes):02}:{int(seconds):02}' if withseconds else f'{int(hours)}:{int(minutes)}'

    def set_static_colors(self, bolt_color:tuple=None, zap_color:tuple=None, spark_color:tuple=None) -> None:

        """
        Sets the static colors of the lightning object's bolt, zap, and spark.
        """

        self.static_bolt_color = bolt_color if bolt_color is not None else self.static_bolt_color
        self.static_zap_color = zap_color if zap_color is not None else self.static_zap_color
        self.static_spark_color = spark_color if spark_color is not None else self.static_spark_color

    def color_strings(self) -> tuple:
            
        """
        Returns the RGB values of the lightning object.
        """

        static_bolt_color = self.timestring.bolts+self.timestring.zaps+"{:02x}".format(self.static_bolt_color[0])+("{:02x}".format(self.static_bolt_color[1]))
        static_zap_color = "{:02x}".format(self.static_zap_color[0])+self.timestring.zaps+self.timestring.sparks+("{:02x}".format(self.static_zap_color[1]))
        static_spark_color = "{:02x}".format(self.static_spark_color[0])+("{:02x}".format(self.static_spark_color[1]))+self.timestring.sparks+self.timestring.charges
        return ("#"+static_bolt_color, \
                "#"+static_zap_color, \
                "#"+static_spark_color)
    
    def strip_charges(self) -> str:

        """
        Returns the timestring without the charges.        
        """
        return self.timestring.__str__().split("|")[0]

    def __str__(self) -> str:
        return str(self.timestring)


class Timestring:

    """
    A class that represents a lightning timestring.
    """
    def __init__(self, timestring:str=None) -> None:
        self.timestring = timestring if timestring is not None else "0~0~0|0"
        try:
            self.bolts = self.timestring.split("~")[0]
            self.zaps = self.timestring.split("~")[1]
            self.sparks = self.timestring.split("~")[2].split("|")[0]
            self.charges = self.timestring.split("|")[1]
            if len(self.charges) > 1:
                raise IndexError
        except IndexError:
            raise ValueError("Invalid timestring.")
        
    def __str__(self) -> str:
        return self.timestring
    
    def get_parts(self):
        return (self.bolts, self.zaps, self.sparks, self.charges)