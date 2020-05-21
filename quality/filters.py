import django_filter
from . import models
from hicdata import models
from nursequalitydata import models
from accounts import models
import hicdata
import nursequalitydata
import datetime

class allfilter (django_filter.Filterset):
    pass
    