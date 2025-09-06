$(document).ready(
    function () {
        var urlParams = new URLSearchParams(window.location.search);
        if (urlParams == "") {
            localStorage.clear();
            $("#filter_state").css("display","none");
        } else {
            $("#filter_state").css("display","inline-block");
        }
        $('input:checkbox').on('click',function (){
            var fav , favs = [];
            $('input:checkbox').each(function () {
                fav = {id:$(this).attr('id'),value : $(this).prop('checked')};
                favs.push(fav);
            });
            localStorage.setItem("favorites",JSON.stringify(favs));
        });
        // var favorites = JSON.parse(localStorage.getItem('favorites'));
        // for (var i = 0; i <favorites.length; i++){
        //     $('#' + favorites[i].id).prop('checked',favorites[i].value);
        var favorites = JSON.parse(localStorage.getItem('favorites'));
        if (favorites) {
            for (var i = 0; i < favorites.length; i++) {
                $('#' + favorites[i].id).prop('checked', favorites[i].value);}
        }
    }
);

function showVal(x) {
    x = x.toString().replace(/\B(?=(\d{3})+(?!\d))/g,",");
    document.getElementById('sel_price').innerText = x;
}

// تابع حذف پارامترهای خط آدرس
function removeURLParameter(url,parameter) {
    var urlparts = url.split('?');
    if (urlparts.length >= 2) {
        var prefix = encodeURIComponent(parameter) + '=';
        var pars = urlparts[1].split(/[&;]/g);
        for (var i = pars.length;i-- > 0;) {
            if (pars[i].lastIndexOf(prefix,0) !== -1) {
                pars.splice(i,1);
            }
        }
       return urlparts[0] + (pars.length > 0 ? '?' + pars.join('&') : '');
    }
    return url;
}

// تابع انتخاب مدل مرتب سازی محصولات
function select_sort() {
    var select_sort_value = $("#select_sort").val();
    var url = removeURLParameter(window.location.href,"sort_type");
    window.location = url + "&sort_type=" + select_sort_value;
}


//shop_cart...........................................
status_of_shop_cart()

function status_of_shop_cart(){
    $.ajax({
        type:'GET',
        url: "/orders/status_of_shop_cart/" ,
        success: function (res) {
            $("#indicator__value").text(res);
        }
    });
}

function add_to_shop_cart(product_id,qty) {
    if (qty===0) {
        qty=$("#product-quantity").val();
        alert(qty);
    }
    $.ajax({
        type:'GET',
        url: "/orders/add_to_shop_cart/" ,
        data: {
            product_id:product_id,
            qty:qty
        },
        success: function (res) {
            alert("کالای مورد نظر به سبد خرید شما اضافه شد");
            status_of_shop_cart()
        }
    });
}


function delete_from_shop_cart(product_id){
    // alert(product_id)
     $.ajax({
        type:"GET",
        url:"/orders/delete_from_shop_cart/",
        data: {
            product_id:product_id,
        },
        success: function (res) {
            alert("کالای مورد نظر از سبد خرید شما حذف شد");
             $("#shop_cart_list").html(res);
             status_of_shop_cart()
        }
    });
}

function update_shop_cart(){
    var product_id_list= []
    var qty_list = []
    $("input[id^='qty_']").each(function (index){
        product_id_list.push($(this).attr('id').slice(4));
        qty_list.push($(this).val());
    });
    $.ajax({
        type:"GET",
        url:"/orders/update_shop_cart/",
        data: {
            product_id_list:product_id_list,
            qty_list:qty_list
        },
        success: function (res) {
            alert("کالای شما آپدیت شد")
            $("#shop_cart_list").html(res);
            status_of_shop_cart()
        }
    });
}
#____________________________________________________________________________
function showCreateCommentForm(productId,commentId,slug) {
    $.ajax({
        type:"GET",
        url: "/cst/create_comment/" + slug ,
        data: {
            productId: productId,
            commentId: commentId,
        },
        success: function (res) {
            $("#btn_" + commentId).hide();
            $("#comment_form_" + commentId).html(res);
        }
    });
}