======================
Verify Nigerian Number
======================

Python Library to determine details of a Nigerian mobile number

Getting started
================

* Install from pip `pip install verify-nigerian-number`

Usage
======

* Get details of a number:
  
    .. code-block:: python

        from models import NigerianNumber
        from enums import NigerianTelco

        number = NigerianNumber(<the number here>)
        number.get_telco()  # Returns the name of telco

        # There are bool methods that determines if the number is for a specific telco
        # You could check this way (using the telco name after is_*):
        number.is_glo()  # Returns True if it's a glo number
        # Or do this:
        number.is_for_telco(NigerianTelco.GLO)  # Returns True if it's a glo number

        # Telcos covered (as contained in enums.NigerianTelco):
        AIRTEL
        GLO
        MTN
        MULTI_LINKS
        NINE_MOBILE
        NTEL
        SMILE
        STARCOMMS
        ZOOMMOBILE

* Enjoy!
