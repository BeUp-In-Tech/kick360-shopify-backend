from django.db import models


class ShopifyStore(models.Model):
    shop_domain = models.CharField(max_length=255)
    access_token = models.TextField()


# class AccessCode(models.Model):

#     order_id = models.CharField(max_length=100)

#     email = models.EmailField()

#     code = models.CharField(max_length=50)

#     created_at = models.DateTimeField(auto_now_add=True)

class AccessCode(models.Model):
    order_id = models.CharField(max_length=255)
    email = models.EmailField()
    code = models.CharField(max_length=50)

    email_sent = models.BooleanField(default=False)  # NEW FIELD

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.code