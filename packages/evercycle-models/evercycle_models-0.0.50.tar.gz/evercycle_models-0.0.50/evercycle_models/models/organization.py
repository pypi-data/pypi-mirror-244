from django.db import models
from evercycle_models.models.address import Address
from evercycle_models.models.contact import Contact


class Organization(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField()
    name = models.CharField(max_length=50)
    address = models.ForeignKey(Address, models.DO_NOTHING)
    parent_org = models.ForeignKey('self', models.DO_NOTHING, db_column='parent_org', blank=True, null=True)
    main_contact = models.ForeignKey(Contact, models.DO_NOTHING)
    tax_id = models.CharField(max_length=50)
    updated_by = models.IntegerField(blank=True,null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    logo_image = models.BinaryField(blank=True, null=True)
    organization_type = models.TextField(blank=True, null=True)  # This field type is a guess.
    logo = models.CharField(max_length=256)

    class Meta:
        db_table = 'organization'
