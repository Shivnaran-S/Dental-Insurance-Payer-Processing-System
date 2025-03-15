from django.db import models

class PayerGroups(models.Model):
    """
    Represents the parent companies or umbrella organizations that own multiple insurance entities.
    """
    name = models.CharField(max_length=255, unique=True, help_text="payer group name")

    def __str__(self):
        return self.name

class Payers(models.Model):
    """
    Represents the specific insurance companies that belong to a payer group.
    """
    name = models.CharField(max_length=255, unique=True, help_text="payer name")
    payer_group = models.ForeignKey(PayerGroups, on_delete=models.CASCADE, related_name='payers', help_text="payer group")

    def __str__(self):
        return self.name

class PayerDetails(models.Model):
    """
    Represents the various ways a payer might be identified in payment documents.
    """
    payer = models.ForeignKey(Payers, on_delete=models.CASCADE, related_name='details', help_text="The payer this detail belongs to.")
    name = models.CharField(max_length=255, help_text="The name of the payer as it appears in the document.")
    payer_number = models.CharField(max_length=50, blank=True, null=True, help_text="The payer number as it appears in the document.")
    tax_id = models.CharField(max_length=50, blank=True, null=True, help_text="The tax ID of the payer as it appears in the document.")

    def __str__(self):
        return f"{self.name} | {self.payer_number} | {self.tax_id}"

    class Meta:
        unique_together = ('name', 'payer_number', 'tax_id')