$(document).ready(function(){
    var img=document.getElementById('img')
    var imgspan=document.getElementById('imgspan')
    var pid = img.getAttribute("src")
     setTimeout(function(){
        if (pid==''){
        imgspan.remove()
    }
    },100)


})