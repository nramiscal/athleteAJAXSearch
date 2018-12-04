from django.db import models

class AthleteManager(models.Manager):
    def validator(self, form):
        print(form)
        errors = {}

        fname = form['fname']
        lname = form['lname']
        # gender = form['gender']
        image_path = form['image_path']
        sport = form['sport']

        if not fname:
            errors['fname'] = "First name is required"
        if not lname:
            errors['lname'] = "Last name is required"
        if not 'gender' in form:
            errors['gender'] = "Gender is required"
        if not image_path:
            errors['image_path'] = "Image path is required"
        if not sport:
            errors['sport'] = "Sport is required"

        # print(errors)

        if not errors:
            athlete = Athlete.objects.create(fname=fname, lname=lname, gender=form['gender'], image_path=image_path, sport=sport)
            return (True, athlete)
        else:
            return (False, errors)

        return (False, errors)


class Athlete(models.Model):
    fname = models.CharField(max_length=255)
    lname = models.CharField(max_length=255)
    gender = models.CharField(max_length=255)
    sport = models.CharField(max_length=255)
    image_path = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = AthleteManager()

    def __repr__(self):
        return f"<Athlete id: {self.id} '{self.fname}'>"
