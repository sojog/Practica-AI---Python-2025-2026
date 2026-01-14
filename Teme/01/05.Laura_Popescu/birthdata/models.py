from django.db import models
from datetime import date
from django.contrib.auth.models import User

class Birthdate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="birthdates")
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    birthdate = models.DateField()
    notes = models.TextField(blank=True, null=True)
    
    # Optional fields for future expansion
    gender = models.CharField(max_length=20, blank=True, null=True)
    relation = models.CharField(max_length=100, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name or ''} ({self.birthdate})"

    @property
    def full_name(self):
        if self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.first_name
    
    @property
    def name(self):
        return self.full_name

    @property
    def initials(self):
        first = self.first_name[0].upper() if self.first_name else ""
        last = self.last_name[0].upper() if self.last_name else ""
        return f"{first}{last}"

    @property
    def age(self):
        today = date.today()
        return today.year - self.birthdate.year - ((today.month, today.day) < (self.birthdate.month, self.birthdate.day))

    @property
    def zodiac_sign(self):
        day = self.birthdate.day
        month = self.birthdate.month
        
        zodiac_dates = [
            (1, 20, "Capricorn"), (2, 19, "Aquarius"), (3, 20, "Pisces"), (4, 20, "Aries"),
            (5, 21, "Taurus"), (6, 21, "Gemini"), (7, 22, "Cancer"), (8, 23, "Leo"),
            (9, 23, "Virgo"), (10, 23, "Libra"), (11, 22, "Scorpio"), (12, 22, "Sagittarius"),
            (12, 31, "Capricorn")
        ]
        
        for m, d, sign in zodiac_dates:
            if month == m:
                if day < d:
                    # Look at previous month tuple
                    # This logic works because the list is sorted by month? 
                    # Actually standard way is simpler:
                    pass
                # Let's use a simpler if/else structure for clarity and robustness
                pass

        # Robust Implementation
        if (month == 1 and day >= 20) or (month == 2 and day <= 18): return "Aquarius"
        if (month == 2 and day >= 19) or (month == 3 and day <= 20): return "Pisces"
        if (month == 3 and day >= 21) or (month == 4 and day <= 19): return "Aries"
        if (month == 4 and day >= 20) or (month == 5 and day <= 20): return "Taurus"
        if (month == 5 and day >= 21) or (month == 6 and day <= 20): return "Gemini"
        if (month == 6 and day >= 21) or (month == 7 and day <= 22): return "Cancer"
        if (month == 7 and day >= 23) or (month == 8 and day <= 22): return "Leo"
        if (month == 8 and day >= 23) or (month == 9 and day <= 22): return "Virgo"
        if (month == 9 and day >= 23) or (month == 10 and day <= 22): return "Libra"
        if (month == 10 and day >= 23) or (month == 11 and day <= 21): return "Scorpio"
        if (month == 11 and day >= 22) or (month == 12 and day <= 21): return "Sagittarius"
        return "Capricorn"

    @property
    def next_birthday_date(self):
        today = date.today()
        # Create birthday for current year
        try:
            this_year_bday = self.birthdate.replace(year=today.year)
        except ValueError:
            # Handle leap year (Feb 29) -> Set to Feb 28 or Mar 1
            this_year_bday = self.birthdate.replace(year=today.year, month=2, day=28)
        
        if this_year_bday < today:
            try:
                return self.birthdate.replace(year=today.year + 1)
            except ValueError:
                return self.birthdate.replace(year=today.year + 1, month=2, day=28)
        return this_year_bday
