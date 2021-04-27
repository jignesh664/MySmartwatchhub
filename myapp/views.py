from django.shortcuts import render,redirect
from .models import Contact,User,Product,Wishlist,Cart,Transaction #5 Models
   
from django.conf import settings 
from django.core.mail import send_mail 

import random
# for Paytm Integration
from .paytm import generate_checksum,verify_checksum
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def index(request):
	return render(request,'index.html')

def contact(request):
	if request.method=="POST":
		Contact.objects.create(
			name=request.POST['name'],
			email=request.POST['email'],
			mobile=request.POST['mobile'],
			remarks=request.POST['remarks'],
			)
		msg="Contact Submit Successfully"
		contacts=Contact.objects.all()
		return render(request,'contact.html',{'contacts':contacts,'msg':msg})
	else:		
		return render(request,'contact.html')	

def signup(request):
	if request.method=="POST":
		try:
			user=User.objects.get(email=request.POST['email'])
			msg='Email Already Exists'
			return render(request,'signup.html',{'msg':msg})
		except:		
			if request.POST['password']==request.POST['cpassword']:
				User.objects.create(
					fname=request.POST['fname'],
					lname=request.POST['lname'],
					mobile=request.POST['mobile'],
					email=request.POST['email'],
					gender=request.POST['gender'],
					password=request.POST['password'],
					cpassword=request.POST['cpassword'],
					address=request.POST['address'],
					image=request.FILES['image'],
					usertype=request.POST['usertype'],

				)

				
				subject = 'OTP For Registration'
				otp=random.randint(1000,9999)
				message = "Hello User,Your OTP for Registration is:" +str(otp)                                                                                      
				email_from = settings.EMAIL_HOST_USER 
				recipient_list = [request.POST['email'],]
				send_mail( subject, message, email_from, recipient_list ) 


				return render(request,'enter_otp.html',{'otp':otp,'email':request.POST['email']})
			else:
				msg="Password and Confirm Password Does Not Matched"
				return render(request,'signup.html',{'msg':msg})

	else:		
		return render(request,'signup.html')	

def login(request):
	if request.method=="POST":
		if request.POST['action']=="Forgot password":
			return render(request,'enter_email.html')
		elif request.POST['action']=='Login':
			try:

				user=User.objects.get(
				email=request.POST['email'],
				password=request.POST['password'],
				)
				if user.usertype=="user":
					wishlist=Wishlist.objects.filter(user=user) #for wishlist ma header ma No.count karva
					cart=Cart.objects.filter(user=user) # for Cart
					request.session['fname']=user.fname
					request.session['email']=user.email
					request.session['image']=user.image.url
					request.session['wishlist_count']=len(wishlist)  #for lenght wishlist ma header ma No.count karva
					request.session['cart_count']=len(cart) # login thay tyre fatch thay 
					return render(request,'index.html')	
				elif user.usertype=='sellar':	
					request.session['fname']=user.fname
					request.session['email']=user.email
					request.session['image']=user.image.url
					return render(request,'sellar_index.html')	

			except:
				msg="Username and Password Invalid"	
				return render(request,'login.html',{'msg':msg})		
		else:
			pass
	return render(request,'login.html')	

def enter_otp(request):
	otp1=request.POST['otp1']
	otp2=request.POST['otp2']
	email=request.POST['email']

	if otp1==otp2:
		user=User.objects.get(email=email)
		user.status=("active")
		user.save()
		msg="User Varify Successfully Done,Please Login Now"
		return render(request,'login.html',{'msg':msg})
	else:
		msg="invalid OTP"	
		return render(request,'enter_otp.html',{'otp':otp1,'email':email,'msg':msg})	

def enter_email(request):
	if request.method=="POST":
		try:
			user=User.objects.get(email=request.POST['email'])
			subject = 'OTP For Forgot Password'
			otp=random.randint(1000,9999)
			message = "Hello User,Your OTP for Forgot Password is:" +str(otp)                                                                                      
			email_from = settings.EMAIL_HOST_USER 
			recipient_list = [request.POST['email'],]
			send_mail( subject, message, email_from, recipient_list )
			return render(request,'forgot_otp.html',{'otp':otp,'email':request.POST['email']})
		except:
			msg="Email Does Not Exists"
			return render(request,'enter_email.html',{'msg':msg})

def varify_forgot_otp(request):
	if request.method=='POST':
		otp1=request.POST['otp1']
		otp2=request.POST['otp2']
		email=request.POST['email']
		if otp1==otp2:
			return render(request,'new_password.html',{'email':email})
		else:
			msg="Entered OTP is invalid"
			return render(request,'forgot_otp.html',{'otp':otp1,'email':email,'msg':msg})

def update_password(request):
	if 	request.method=='POST':
		user=User.objects.get(email=request.POST['email'])
		if request.POST['npassword']==request.POST['cnpassword']:
			user.password=request.POST['npassword']
			user.cpassword=request.POST['npassword']
			user.save()
			msg="Password Successfully updated"
			return render(request,'login.html',{'msg':msg})
		else:
			msg='New Password and Confirm New Password Does not Matched'
			return render(request,'new_password.html',{'email':request.POST['email'],'msg':msg})


def logout(request):
	try:
		del request.session['email']
		del request.session['fname']
		del request.session['image']
		return render(request,'login.html')
	except:
		pass

def change_password(request):
	if request.method=='POST':
		user=User.objects.get(email=request.session['email'])
		if user.password==request.POST['old_password']:
			if request.POST['npassword']==request.POST['cnpassword']:
				user.password=request.POST['npassword']
				user.cpassword=request.POST['npassword'] #or [cnpassword] bcz both eqal already confirm
				user.save()
				return redirect('logout')

			else:
				msg="New Password and Confirm New Password Does Matched"
				return render(request,'change_password.html',{'msg':msg})

		else:
			msg="Old Password Incorrect"
			return render(request,'change_password.html',{'msg':msg})		
	else:
		return render(request,'change_password.html')		

def edit_profile(request):
	user=User.objects.get(email=request.session['email'])  #old data
	if request.method=="POST":
		user.fname=request.POST['fname']
		user.lname=request.POST['lname']
		user.mobile=request.POST['mobile']
		user.email=request.POST['email']
		user.address=request.POST['address']
		user.gender=request.POST['gender']
		try:
			user.image=request.FILES['image']
			user.save()
			user=User.objects.get(email=request.session['email'])
			msg="Profile Saved Successfully"
			request.session['image']=user.image.url
			return render(request,'edit_profile.html',{'user':user,'msg':msg})
		except:
			user.save()
			user=User.objects.get(email=request.session['email'])
			msg="Profile Saved Successfully"
			return render(request,'edit_profile.html',{'user':user,'msg':msg})
	else:		
		return render(request,'edit_profile.html',{'user':user})

def sellar_index(request):
	return render(request,'sellar_index.html')		

def sellar_edit_profile(request):
	user=User.objects.get(email=request.session['email'])  #old data
	if request.method=="POST":
		user.fname=request.POST['fname']
		user.lname=request.POST['lname']
		user.mobile=request.POST['mobile']
		user.email=request.POST['email']
		user.address=request.POST['address']
		user.gender=request.POST['gender']
		try:
			user.image=request.FILES['image']
			user.save()
			user=User.objects.get(email=request.session['email'])
			msg="Profile Saved Successfully"
			request.session['image']=user.image.url
			return render(request,'sellar_edit_profile.html',{'user':user,'msg':msg})
		except:
			user.save()
			user=User.objects.get(email=request.session['email'])
			msg="Profile Saved Successfully"
			return render(request,'sellar_edit_profile.html',{'user':user,'msg':msg})
	else:		
		return render(request,'sellar_edit_profile.html',{'user':user})

def sellar_change_password(request):
	if request.method=='POST':
		user=User.objects.get(email=request.session['email'])
		if user.password==request.POST['old_password']:
			if request.POST['npassword']==request.POST['cnpassword']:
				user.password=request.POST['npassword']
				user.cpassword=request.POST['npassword'] #or [cnpassword] bcz both eqal already confirm
				user.save()
				return redirect('logout')

			else:
				msg="New Password and Confirm New Password Does Matched"
				return render(request,'sellar_change_password.html',{'msg':msg})

		else:
			msg="Old Password Incorrect"
			return render(request,'sellar_change_password.html',{'msg':msg})		
	else:
		return render(request,'sellar_change_password.html')	


def sellar_add_product(request):
	if request.method=="POST":
		sellar=User.objects.get(email=request.session['email'])
		Product.objects.create(
			sellar=sellar,
			product_brand=request.POST['product_brand'],
			product_model=request.POST['product_model'],
			product_price=request.POST['product_price'],
			product_disc=request.POST['product_disc'],
			product_image=request.FILES['product_image'],

			)
		msg="Add Product Successfully"
		return render(request,'sellar_add_product.html',{'msg':msg})
	else:
		return render(request,'sellar_add_product.html')


def sellar_view_product(request):
	sellar=User.objects.get(email=request.session['email'])
	products=Product.objects.filter(sellar=sellar) # particular sellar view karva
	#products=Product.objects.all() if all sellar view in sellar page 
	return render(request,'sellar_view_product.html',{'products':products})


def sellar_product_detail(request,pk):
	product=Product.objects.get(pk=pk)
	return render(request,'sellar_product_detail.html',{'product':product})

def sellar_edit_product(request,pk):
	product=Product.objects.get(pk=pk)
	if request.method=='POST':
		product.product_model=request.POST['product_model']
		product.product_price=request.POST['product_price']
		product.product_disc=request.POST['product_disc']
		
		
		try:
			product.product_image=request.FILES['product_image']
			product.save()
			return redirect('sellar_view_product')
		except:
			product.save()
			return redirect('sellar_view_product')		

	else:		
		return render(request,'sellar_edit_product.html',{'product':product})

def sellar_delete_product(request,pk):
	product=Product.objects.get(pk=pk)
	product.delete()
	return redirect('sellar_view_product')

def user_view_product(request,pb):
	#print(pb)
	if pb=='all':
		products=Product.objects.all()
		return render(request,'user_view_product.html',{'products':products})
	else:

		products=Product.objects.filter(product_brand=pb)
		return render(request,'user_view_product.html',{'products':products})

def user_product_detail(request,pid):
	flag=False     #for wishlist                  # 2 button se to je vastu add to wishlist ma hoy to na aave,
	flag1=False    # cart     
	user=User.objects.get(email=request.session['email'])
	product=Product.objects.get(pk=pid)
	try:
		Wishlist.objects.get(user=user,product=product)   #for wishlist fatch 
		flag=True
	except:
		pass
	try:
		Cart.objects.get(user=user,product=product)   #for wishlist fatch 
		flag1=True
	except:
		pass		
	return render(request,'user_product_detail.html',{'product':product,'flag':flag,'flag1':flag1})

def add_to_wishlist(request,pk):
	pr=Product.objects.get(pk=pk)
	u=User.objects.get(email=request.session['email'])
	Wishlist.objects.create(user=u,product=pr)
	return redirect('mywishlist')

def mywishlist(request):
	user=User.objects.get(email=request.session['email'])
	wishlist=Wishlist.objects.filter(user=user)
	request.session['wishlist_count']=len(wishlist) # for wishlist header mathi remove or update karva

	return render(request,'mywishlist.html',{'wishlist':wishlist})

def remove_from_wishlist(request,pk):
	user=User.objects.get(email=request.session['email'])
	product=Product.objects.get(pk=pk)
	wishlist=Wishlist.objects.get(user=user,product=product)
	wishlist.delete()
	return redirect('mywishlist')

def mycart(request):
	net_price=0                                              # write after Add_to product but add now upp 
	user=User.objects.get(email=request.session['email'])
	cart=Cart.objects.filter(user=user)
	# for 358 and 359 line for Checkout netprice 
	for i in cart:
		net_price=net_price+int(i.total_price)

	request.session['cart_count']=len(cart)
	return render(request,'mycart.html',{'cart':cart,'net_price':net_price})	

def add_to_cart(request,pk):	
	product=Product.objects.get(pk=pk)
	user=User.objects.get(email=request.session['email'])
	Cart.objects.create(
		user=user,
		product=product,
		price=product.product_price,
		total_price=product.product_price,

		)
	return redirect('mycart')

def remove_from_cart(request,pk):
	user=User.objects.get(email=request.session['email'])
	product=Product.objects.get(pk=pk)
	cart=Cart.objects.get(user=user,product=product)	
	cart.delete()
	return redirect('mycart')

def change_qty(request):
	cart=Cart.objects.get(pk=request.POST['pk'])
	qty=request.POST['qty']
	cart_qty=qty
	cart.total_price=int(cart.price)*int(qty)      #price and qty multiply qty string se to int ma convert
	cart.save()
	return redirect('mycart')



# for Paytm Integration

def initiate_payment(request):
    try:
    	user=User.objects.get(email=request.session['email'])
    	amount = int(request.POST['amount'])
    except:
        return render(request, 'mycart.html', context={'error': 'Wrong Accound Details or amount'})

    transaction = Transaction.objects.create(made_by=user, amount=amount)
    transaction.save()
    merchant_key = settings.PAYTM_SECRET_KEY

    params = (
        ('MID', settings.PAYTM_MERCHANT_ID),
        ('ORDER_ID', str(transaction.order_id)),
        ('CUST_ID', str(transaction.made_by.email)),
        ('TXN_AMOUNT', str(transaction.amount)),
        ('CHANNEL_ID', settings.PAYTM_CHANNEL_ID),
        ('WEBSITE', settings.PAYTM_WEBSITE),
        # ('EMAIL', request.user.email),
        # ('MOBILE_N0', '9911223388'),
        ('INDUSTRY_TYPE_ID', settings.PAYTM_INDUSTRY_TYPE_ID),
        ('CALLBACK_URL', 'http://127.0.0.1:8000/callback/'),
        # ('PAYMENT_MODE_ONLY', 'NO'),
    )

    paytm_params = dict(params)
    checksum = generate_checksum(paytm_params, merchant_key)

    transaction.checksum = checksum
    transaction.save()

    paytm_params['CHECKSUMHASH'] = checksum
    print('SENT: ', checksum)
    return render(request, 'redirect.html', context=paytm_params)

@csrf_exempt
def callback(request):
    if request.method == 'POST':
        received_data = dict(request.POST)
        paytm_params = {}
        paytm_checksum = received_data['CHECKSUMHASH'][0]
        for key, value in received_data.items():
            if key == 'CHECKSUMHASH':
                paytm_checksum = value[0]
            else:
                paytm_params[key] = str(value[0])
        # Verify checksum
        is_valid_checksum = verify_checksum(paytm_params, settings.PAYTM_SECRET_KEY, str(paytm_checksum))
        if is_valid_checksum:
            received_data['message'] = "Checksum Matched"
        else:
            received_data['message'] = "Checksum Mismatched"
            return render(request, 'callback.html', context=received_data)
        return render(request, 'callback.html', context=received_data)



	


