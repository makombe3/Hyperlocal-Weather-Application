from django.db import models

NEIGHBORHOODS = [
    ("Mount Pleasant", "Mount Pleasant"),
    ("Avondale", "Avondale"),
    ("Borrowdale", "Borrowdale"),
    ("Highfield", "Highfield"),
    ("Eastlea", "Eastlea"),
    ("Hatcliffe", "Hatcliffe"),
    ("Ruwa", "Ruwa"),
    ("Epworth", "Epworth"),
    ("Glen Lorne", "Glen Lorne"),
    ("Chishawasha", "Chishawasha"),
]

class WeatherReport(models.Model):
    datetime = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=32, choices=NEIGHBORHOODS)
    precipitation = models.FloatField(null=True, blank=True)
    humidity = models.FloatField(null=True, blank=True)
    cloudcover = models.FloatField(null=True, blank=True)
    tempmin = models.FloatField(null=True, blank=True)
    temp = models.FloatField(null=True, blank=True)
    dew = models.FloatField(null=True, blank=True)
    windspeed = models.FloatField(null=True, blank=True)
    winddir = models.FloatField(null=True, blank=True)
    sealevelpressure = models.FloatField(null=True, blank=True)
    precipcover = models.FloatField(null=True, blank=True)
    rain = models.BooleanField()
    comment = models.TextField(blank=True)

    def __str__(self):
        return f"{self.location} @ {self.datetime}"
