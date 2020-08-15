from django.db import models
from accounts.models import Account


class Category(models.Model):

    tag = models.CharField(max_length=50, default='')
    image = models.ImageField(upload_to="media/", default='')
    URL = models.TextField(default='', null=True)
    class Meta:

        verbose_name_plural = 'Category'

    def __str__(self):
        return self.tag


class Product(models.Model):

    owner = models.ForeignKey(Account,on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=50, default='')
    image = models.ImageField(upload_to="media/", default='')
    price = models.CharField(default='', max_length=50)
    detail = models.TextField(default='', blank=True)
    URL = models.TextField(default='', null=True)
    tags = models.ManyToManyField(Category)
    hashtags = models.TextField(null=True)
    count = models.IntegerField(default=1)

    class Meta:

        verbose_name_plural = 'Products'

    def __str__(self):

        return self.title


class Comments(models.Model):

    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    text = models.TextField(default='')
    date = models.DateTimeField(auto_now=True)

    class Meta:

        verbose_name_plural = 'Comments'

    def __str__(self):

        return '{} - {}'.format(self.product.title, self.user)


class Likes(models.Model):

    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    comment = models.ForeignKey(Comments, on_delete=models.CASCADE)
    like = models.CharField(max_length=150, choices=[('like', 'like'), ('dislike', 'dislike')])


    class Meta:

        verbose_name_plural = 'Likes'

    def __str__(self):

        return '{} - {}'.format(self.user, self.like)


class Rate(models.Model):

    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rate = models.CharField(max_length=150, choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')])

    class Meta:

        verbose_name_plural = 'Rate'

    def __str__(self):

        return '{} - {} - {}'.format(self.user, self.product.title, self.rate)
