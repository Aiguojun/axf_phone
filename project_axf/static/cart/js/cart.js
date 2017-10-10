$(document).ready(function(){
     //修改购物车
    var addShoppings = document.getElementsByClassName("addShopping")
    var subShoppings = document.getElementsByClassName("subShopping")

    for (var i = 0; i < addShoppings.length; i++){
        addShopping = addShoppings[i]
        addShopping.addEventListener("click", function(){
            pid = this.getAttribute("ga")
            $.post("/changecart/0/",{"productid":pid}, function(data){
                if (data.status == "success"){
                    //添加成功，把中间的span的innerHTML变成当前的数量
                    document.getElementById(pid).innerHTML = data.data
                    document.getElementById(pid+'price').innerHTML=data.price
                }
            })
        })
    }


    for (var i = 0; i < subShoppings.length; i++){
        subShopping = subShoppings[i]
        subShopping.addEventListener("click", function(){
            pid = this.getAttribute("ga")
            $.post("/changecart/1/",{"productid":pid}, function(data){
                if (data.status == "success"){
                    //添加成功，把中间的span的innerHTML变成当前的数量
                    document.getElementById(pid).innerHTML = data.data
                    document.getElementById(pid+'price').innerHTML=data.price
                }

                if (data.data==0){
                    //删除document元素
                    var li=document.getElementById(pid+'li')
                    li.parentNode.removeChild(li)
                }
            })
        })
    }

    //单选
    var ischoses=document.getElementsByClassName('ischose')
    for(j=0;j<ischoses.length;j++){
        ischose=ischoses[j]
        ischose.addEventListener('click',function(){
            pid = this.getAttribute("goodsid")
            $.post('/changecart/2/',{'productid':pid},function(data){
                var choice=document.getElementById(pid+'a')
                    choice.innerHTML=data.data
                var all_money=document.getElementById('all_money')
                if (data.status=='success'){

                    if (data.is_chose){
                        var n=$('#all_money').html()
                        if(n!='NaN'){
                            all_money.innerHTML=parseFloat(n)+parseFloat(data.price)
                        }
                        if(n==''){
                            all_money.innerHTML=data.price
                        }

                    }

                    else
                    {
                    var n=$('#all_money').html()
                        if(n>0){
                            all_money.innerHTML=parseFloat(n)-parseFloat(data.price)
                        }

                    }

                }


            },false)

        },false)

    }


    var ok=document.getElementById('ok')
    ok.addEventListener('click',function(){
        var f=confirm('是否下单?')
        if (f){
            $.post("/saveorder/", function(data){
                if (data.status = "success"){
                    window.location.href = "http://127.0.0.1:8000/cart/"
                }
            })
        }

    })


    //全选点击事件
    var all_choice=document.getElementById('confirmspan')
    all_choice.addEventListener('click',function(){


       var ischoses=document.getElementsByClassName('ischose')
       for(j=0;j<ischoses.length;j++){
            ischose=ischoses[j]

            pid = ischose.getAttribute("goodsid")
            $.post('/changecart/3/',{'productid':pid},function(data){

                if(data.status=='success'){
                      var choice=document.getElementById(data.pid+'a')
                      choice.innerHTML=data.data

                      var all_money=document.getElementById('all_money')

                      var n=$('#all_money').html()
                        if(n!='NaN'){
                            all_money.innerHTML=parseFloat(n)+parseFloat(data.price)
                        }
                        if(n==''){
                            all_money.innerHTML=data.price
                        }
                }


            },false)

       }


       var choiceright=document.getElementById('choiceright')
       $.post('/allchoice/',function(data){
             //var choiceright=document.getElementById('choiceright')
             choiceright.innerHTML=data.data

       })
       var k=$('#choiceright').html()
       if ($('#choiceright').html()=="√"){
            var ischoses=document.getElementsByClassName('ischose')

            for(j=0;j<ischoses.length;j++){
                ischose=ischoses[j]

                pid = ischose.getAttribute("goodsid")
                $.post('/changecart/3/',{'productid':pid},function(data){

                    if(data.status=='success'){
                          var choice=document.getElementById(data.pid+'a')
                              choice.innerHTML=data.data

                          var n=$('#all_money').html()
                           if(n>0){
                            all_money.innerHTML=0
                            }
                    }


                },false)

            }

       }

    })
})