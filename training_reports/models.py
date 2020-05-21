from django.db import models
from django.forms import ModelForm
from django import forms
from accounts.models import Departments
from accounts.models import Doctors
from accounts.models import Locations
from django.core.exceptions import FieldError
import datetime
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.conf import settings
