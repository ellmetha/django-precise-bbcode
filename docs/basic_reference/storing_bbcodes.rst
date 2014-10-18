###############
Storing BBCodes
###############

The Django built-in ``models.TextField`` is all you need to simply add BBCode contents to your models. However, a common need is to store both the BBCode content and the corresponding HTML markup in the database. To address this *django-precise-bbcode* provides a ``BBCodeTextField``::

    from django.db import models
    from precise_bbcode.fields import BBCodeTextField

    class Post(models.Model):
        content = BBCodeTextField()

A ``BBCodeTextField`` field contributes two columns to the model instead of a standard single column : one is used to save the BBCode content ; the other one keeps the corresponding HTML markup. The HTML content of such a field can then be displayed in any template by using its rendered attribute::

    {{ post.content.rendered }}
