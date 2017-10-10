$(document).ready(function(){
    setTimeout(function(){
           swiper1()
           swiperMenu1()
    },100)


})

function swiperMenu1(){
    var swiperMenu1=new Swiper('#swiperMenu',{
        slidesPerView:3,
        paginationClickable:true,
        spaceBetween:2,
        loop:false,
    })

}


function swiper1(){
    var swiper1=new Swiper('#topSwiper',{
        direction:'horizontal',
        loop:true,
        speed:500,
        autoplay:2000,
        pagination:'.swiper-pagination',
        control:true,
    })

}