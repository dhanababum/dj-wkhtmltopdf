from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator


class PaperSizeFormat(object):
    """
    Page Sizes
    """
    A0 = 'A0'
    A1 = 'A1'
    A2 = 'A2'
    A3 = 'A3'
    A4 = 'A4'
    A5 = 'A5'
    A6 = 'A6'
    A7 = 'A7'
    A8 = 'A8'
    A9 = 'A9'
    B0 = 'B0'
    B1 = 'B1'
    B2 = 'B2'
    B3 = 'B3'
    B4 = 'B4'
    B5 = 'B5'
    B6 = 'B6'
    B7 = 'B7'
    B8 = 'B8'
    B9 = 'B9'
    B10 = 'B10'
    C5E = 'C5E'
    COMM10E = 'Comm10E'
    DLE = 'DLE'
    EXECUTIVE = 'Executive'
    FOLIO = 'Folio'
    LEDGER = 'Ledger'
    LEGAL = 'Legal'
    LETTER = 'Letter'
    TABLOID = 'Tabloid'
    FORMAT = [
        (A0, 'A0  5   841 x 1189 mm'),
        (A1, 'A1  6   594 x 841 mm'),
        (A2, 'A2  7   420 x 594 mm'),
        (A3, 'A3  8   297 x 420 mm'),
        (A4, 'A4  0   210 x 297 mm, 8.26 x 11.69 inches'),
        (A5, 'A5  9   148 x 210 mm'),
        (A6, 'A6  10  105 x 148 mm'),
        (A7, 'A7  11  74 x 105 mm'),
        (A8, 'A8  12  52 x 74 mm'),
        (A9, 'A9  13  37 x 52 mm'),
        (B0, 'B0  14  1000 x 1414 mm'),
        (B1, 'B1  15  707 x 1000 mm'),
        (B2, 'B2  17  500 x 707 mm'),
        (B3, 'B3  18  353 x 500 mm'),
        (B4, 'B4  19  250 x 353 mm'),
        (B5, 'B5  1   176 x 250 mm, 6.93 x 9.84 inches'),
        (B6, 'B6  20  125 x 176 mm'),
        (B7, 'B7  21  88 x 125 mm'),
        (B8, 'B8  22  62 x 88 mm'),
        (B9, 'B9  23  33 x 62 mm'),
        (B10, 'B10    16  31 x 44 mm'),
        (C5E, 'C5E 24  163 x 229 mm'),
        (COMM10E, 'Comm10E 25  105 x 241 mm, U.S. Common 10 Envelope'),
        (DLE, 'DLE 26 110 x 220 mm'),
        (EXECUTIVE, 'Executive 5   7.5 x 10 inches, 190.5 x 254 mm'),
        (FOLIO, 'Folio 27  210 x 330 mm'),
        (LEDGER, 'Ledger  28  431.8 x 279.4 mm'),
        (LEGAL, 'Legal  3  8.5 x 14 inches, 215.9 x 355.6 mm'),
        (LETTER, 'Letter 2 8.5 x 11 inches, 215.9 x 279.4 mm'),
        (TABLOID, 'Tabloid 29 279.4 x 431.8 mm'),
    ]


class HtmlHeaderFooter(models.Model):
    """ It is the model for allowing to craete html header, footer and wkhtmltopdf options.
    """
    LANDSCAPE = 'Landscape'
    PORTRAIT = 'Portrait'
    ORIENTATION_CHOICES = ((LANDSCAPE, 'Landscape'), (PORTRAIT, 'Portrait'))
    name = models.CharField(verbose_name="Html Name", max_length=100)
    header = models.TextField(
        verbose_name="Html Header",
        blank=True, null=True)
    footer = models.TextField(
        verbose_name="Html Footer",
        blank=True, null=True)
    css = models.TextField(verbose_name="Html Css", blank=True, null=True)
    quiet = models.BooleanField(verbose_name="Quiet", default=True)
    margin_top = models.DecimalField(
        verbose_name="Top Margin (mm)",
        blank=True,
        null=True,
        max_digits=5, decimal_places=2, validators=[MinValueValidator(0.0)])
    margin_bottom = models.DecimalField(
        verbose_name="Bottom Margin (mm)",
        blank=True,
        null=True,
        max_digits=5, decimal_places=2, validators=[MinValueValidator(0.0)])
    margin_left = models.DecimalField(
        verbose_name="Left Margin (mm)",
        blank=True,
        null=True,
        max_digits=5, decimal_places=2, validators=[MinValueValidator(0.0)])
    margin_right = models.DecimalField(
        verbose_name="Right Margin (mm)",
        blank=True,
        null=True,
        max_digits=5, decimal_places=2, validators=[MinValueValidator(0.0)])
    orientation = models.CharField(
        choices=ORIENTATION_CHOICES,
        blank=True,
        max_length=20)
    zoom = models.DecimalField(
        verbose_name="zoom",
        blank=True,
        null=True,
        max_digits=5, decimal_places=2, validators=[MinValueValidator(0.0)])
    page_size = models.CharField(choices=PaperSizeFormat.FORMAT, max_length=20)
    encode_type = models.CharField(max_length=10, default='utf-8')

    class Meta:
        app_label = 'djwkhtmltopdf'

    def __unicode__(self,):
        return self.name


class HtmlBody(models.Model):
    """It is the model for allowing to create different html bodies.
    """
    name = models.CharField(max_length=20, verbose_name="Html Body Name")
    body = models.TextField(verbose_name="Html Body")

    class Meta:
        app_label = 'djwkhtmltopdf'

    def __unicode__(self,):
        return self.name


class Html(models.Model):
    """
    html object
    """
    htmlheader = models.ForeignKey(HtmlHeaderFooter)
    htmlbody = models.ManyToManyField(HtmlBody)
    name = models.CharField(
        max_length=20,
        verbose_name="Pdf Name", blank=True, null=True)
    view = models.CharField(max_length=150)
    attachment = models.BooleanField(default=True)

    class Meta:
        app_label = 'djwkhtmltopdf'

    def clean(self):
        if len(self.name) == 0 and self.name.isspace():
            raise ValidationError("PDF name should more than two letters.")

    def __unicode__(self,):
        return self.name
