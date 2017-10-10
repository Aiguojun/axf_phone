# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .forms.login import LoginForms
from django.http import JsonResponse
from django.shortcuts import render,redirect
from .models import Wheel,Nav,Mustbuy,Shop,MainShow,FoodTypes,Goods,User,Cart,Order
import time,random,os
from django.conf import settings
from django.contrib.auth import logout
# Create your views here.
def home(request):
    wheelsList=Wheel.objects.all()
    navList=Nav.objects.all()
    mustbuy=Mustbuy.objects.all()
    shopList=Shop.objects.all()
    shop1=shopList[0]
    shop2=shopList[1:3]
    shop3 = shopList[3:7]
    shop4 = shopList[7:12]
    mainList=MainShow.objects.all()
    return render(request,'axf/home.html',locals())

def market(request,categoryid1,cid,sortid):
    leftList=FoodTypes.objects.all()

    if cid=='0':
        productList = Goods.objects.filter(categoryid=categoryid1)
    else:
        productList = Goods.objects.filter(categoryid=categoryid1,childcid=cid)

    if sortid=='1':
        productList=productList.order_by('productnum')
    elif sortid=='2':
        productList=sorted(productList,key=lambda item:float(item.price))
    else:
        productList = sorted(productList, key=lambda item: float(item.price),reverse=True)

    group=leftList.get(typeid=categoryid1)
    childList=[]
    childnames=group.childtypenames
    arr1=childnames.split('#')
    for str in arr1:
        arr2=str.split(':')
        obj={'childName':arr2[0],'childId':arr2[1]}
        childList.append(obj)

    categoryid = categoryid1
    cid=cid
    #显示cart里已经存在的数量
    cartlist=[]
    token=request.session.get('token')
    if token:
        #login
        user=User.objects.get(userToken=token)
        cartlist=Cart.objects.filter(userAccount=user.userAccount)

    for p in productList:
        for c in cartlist:
            if p.productid==c.productid:
                p.num=c.productnum

    return render(request,'axf/market.html',locals())

def cart(request):
    title='购物车'
    cartslist = []
    token = request.session.get("token")
    if token != None:
        user = User.objects.get(userToken=token)
        cartslist = Cart.objects.filter(userAccount=user.userAccount)
        people=user.userName
        iphone=user.userPhone
        address=user.userAdderss

    return render(request,'axf/cart.html',locals())

def changecart(request,flag):
    #判断是否登陆
    token=request.session.get('token')
    if token==None:
        # 没登录
        return JsonResponse({'data':'-1','status':'error'})
    productid=request.POST.get('productid')
    user=User.objects.get(userToken=token)
    product=Goods.objects.get(productid=productid)

    if flag=='0':
        if product.storenums == 0:
            return JsonResponse({'data': -2, 'status': 'error'})
        carts=Cart.objects.filter(userAccount=user.userAccount)
        c=None
        if carts.count()==0:
            # 直接增加一条订单

            c=Cart.createcart(user.userAccount,productid,1,product.price,
                              True,product.productimg,product.productlongname,False)
            c.save()
        else:
            try:
                c=carts.get(productid=productid)
                #修改数量和价格
                c.productnum+=1
                c.productprice='%.2f'%(float(product.price)*c.productnum)
                c.save()
            except Cart.DoesNotExist as e:
                #直接增加一条订单
                c = Cart.createcart(user.userAccount, productid, 1, product.price,
                                    True, product.productimg, product.productlongname, False)
                c.save()

        #库存减一
        product.storenums-=1
        product.save()
        return JsonResponse({'data':c.productnum,'status':'success','price':c.productprice})
    elif flag=='1':
        if product.storenums == 0:
            return JsonResponse({'data': -2, 'status': 'error'})
        carts = Cart.objects.filter(userAccount=user.userAccount)
        c = None
        if carts.count() == 0:
           return JsonResponse({'data':-2,'status':'error'})
        else:
            try:
                c = carts.get(productid=productid)
                # 修改数量和价格
                c.productnum -= 1
                c.productprice = '%.2f' % (float(product.price) * c.productnum)
                c.save()
                if c.productnum==0:
                    c.delete()
                else:
                    c.save()
            except Cart.DoesNotExist as e:
                return JsonResponse({'data': -2, 'status': 'error'})

        # 库存
        product.storenums += 1
        product.save()
        return JsonResponse({'data': c.productnum, 'status': 'success','price':c.productprice})

    elif flag=='2':
        carts=Cart.objects.filter(userAccount=user.userAccount)
        c=carts.get(productid=productid)

        c.isChose=not c.isChose
        c.save()
        str=''
        if c.isChose:
            str="√"
        price = '%.2f' % (float(product.price) * c.productnum)
        return JsonResponse({'data':str,'status':'success','price':price,'is_chose':c.isChose})
    elif flag == '3':
        trueFlag = request.session.get('trueFlag')
        carts = Cart.objects.filter(userAccount=user.userAccount)
        c = carts.get(productid=productid)
        price = '%.2f' % (float(product.price) * c.productnum)
        if trueFlag=='':
            if not c.isChose :
                c.isChose = not c.isChose
            c.save()
            str = "√"

            return JsonResponse({'data': str, 'status': 'success', 'pid': productid,'price':price})
        if trueFlag=="√":
            if c.isChose:
                c.isChose = not c.isChose
            c.save()
            str = ''

            return JsonResponse({'data': str, 'status': 'success', 'pid': productid,'price':price})

def allchoice(request):
    trueFlag=request.session.get('trueFlag')
    token=request.session.get('token')
    if token==None:
       return JsonResponse({'data': -2, 'status': 'error'})
    if trueFlag=='':
        trueFlag ="√"
    elif trueFlag == "√":
        trueFlag=''
    request.session['trueFlag']=trueFlag
    return JsonResponse({'data': trueFlag, 'status': 'success'})







def mine(request):
    username=request.session.get('username','未登陆')

    token=request.session.get('token')
    if token:
        user=User.objects.get(userToken=token)
        imgpath=user.userImg
    return render(request,'axf/mine.html',locals())

def quit(request):
    logout(request)
    return redirect('axf:mine')


def login(request):
    if request.method=='POST':
        f=LoginForms(request.POST)
        if f.is_valid():
            nameid=f.cleaned_data['username']
            passwd=f.cleaned_data['passwd']

            try:
                user=User.objects.get(userAccount=nameid)
                if user.userPasswd!=passwd:
                    return redirect('axf:login')

            except User.DoesNotExist as e:
                return redirect('axf:login')

            token = time.time() + random.randrange(1, 100000)
            user.userToken = str(token)
            user.save()
            request.session['username'] = user.userName
            request.session['token'] = user.userToken
            request.session['trueFlag'] = "√"
            imgpath=user.userImg
            return redirect( "/mine/",{'imgpath':imgpath})

        else:
            return render(request,'axf/login.html',{'title':'登陆','form':f,'error':f.errors})

    else:
        f=LoginForms()
        return render(request,'axf/login.html',{'title':'登陆','form':f})

def register(request):
    if request.method == "POST":
        userAccount = request.POST.get("userAccount")
        userPasswd = request.POST.get("userPass")
        userName = request.POST.get("userName")
        userPhone = request.POST.get("userPhone")
        userAdderss = request.POST.get("userAdderss")
        userRank = 0
        token = time.time() + random.randrange(1, 100000)
        userToken = str(token)
        f=request.FILES['userImg']
        userImg=os.path.join(settings.MEDIA_ROOT,userAccount+'.png')
        with open(userImg,'wb') as fp:
            for data in f.chunks():
                fp.write(data)

        user = User.createuser(userAccount, userPasswd, userName, userPhone, userAdderss, userImg, userRank, userToken)
        user.save()

        request.session['username']=userName
        request.session['token']=userToken

        return redirect('axf:mine')
    else:
        return render(request, 'axf/register.html', {"title": "注册"})



def checkuserid(request):
    userid=request.POST.get('userid')
    try:
        user=User.objects.get(userAccount=userid)
        return JsonResponse({'data':'该用户已经注册','status':'error'})
    except User.DoesNotExist as e:

        return JsonResponse({'data':'ok','status':'success'})


def saveorder(request):
    token=request.session.get('token')
    if token==None:
        return JsonResponse({'status':'error'})

    user=User.objects.get(userToken=token)
    carts=Cart.objects.filter(isChose=True)
    if carts.count()==0:
        return JsonResponse({'data':-1,'status':'error'})

    oid=time.time()+random.randrange(1,1000)
    oid='%d'%oid
    o=Order.createorder(oid,user.userAccount,0)
    o.save()
    for cart in carts:
        cart.isDelete=True
        cart.orderid=oid
        cart.save()

    return JsonResponse({'status':'success'})