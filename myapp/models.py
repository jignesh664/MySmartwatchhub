from django.db import models
from django.utils import timezone
# Create your models here.
class Contact(models.Model):
	name=models.CharField(max_length=100)
	email=models.CharField(max_length=100)
	mobile=models.CharField(max_length=100)
	remarks=models.TextField()

class User(models.Model):
	fname=models.CharField(max_length=100)
	lname=models.CharField(max_length=100)
	mobile=models.CharField(max_length=100)
	email=models.EmailField()
	GENDER_CHOICES = (('M', 'male'),('F', 'female'),)
	gender=models.CharField(max_length=2,choices=GENDER_CHOICES)
	password=models.TextField()
	cpassword=models.TextField()
	address=models.CharField(max_length=100)
	status=models.CharField(max_length=100,default="inactive")
	image=models.ImageField(upload_to="image/",blank=True,null=True) #or default
	usertype=models.CharField(max_length=100,default="user")


	def __str__(self):
		return self.fname+" "+self.lname

class Product(models.Model):

	BRAND=(
			('Apple','Apple'),
			('Samsung','Samsung'),
			('MI','MI'),
			('Fitbit','Fitbit'),
			('Fasttrack','Fasttrack'),
			('Realme','Realme'),
			('Fossil','Fossil'),
			('Amazefit','Amazefit'),
			('Noise','Noise'),

		)
	sellar=models.ForeignKey(User,on_delete=models.CASCADE)
	product_brand=models.CharField(max_length=100,choices=BRAND)
	product_model=models.CharField(max_length=100)
	product_price=models.IntegerField()
	product_disc=models.TextField()
	product_image=models.ImageField(upload_to="product_image")

	def __str__(self):
		return self.sellar.fname+" -"+self.product_model

class Wishlist(models.Model):
	user=models.ForeignKey(User,on_delete=models.CASCADE)
	product=models.ForeignKey(Product,on_delete=models.CASCADE)
	date=models.DateTimeField(default=timezone.now)


	def __str__(self):
		return self.user.fname+" -"+ self.product.product_brand

class Cart(models.Model):
	user=models.ForeignKey(User,on_delete=models.CASCADE)
	product=models.ForeignKey(Product,on_delete=models.CASCADE)
	date=models.DateTimeField(default=timezone.now)
	qty=models.IntegerField(default=1)
	price=models.IntegerField()
	total_price=models.IntegerField()

	def __str__(self):
		return self.user.fname+" -"+ self.product.product_brand

# for Paytm Integration 

class Transaction(models.Model):
    made_by = models.ForeignKey(User, related_name='transactions',on_delete=models.CASCADE)
    made_on = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField()
    order_id = models.CharField(unique=True, max_length=100, null=True, blank=True)
    checksum = models.CharField(max_length=100, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.order_id is None and self.made_on and self.id:
            self.order_id = self.made_on.strftime('PAY2ME%Y%m%dODR') + str(self.id)
        return super().save(*args, **kwargs)


    def __str__(self):
       	return self.made_by.fname+" "+self.made_by.lname


