`use strict`
window.onload = function () {
    document.querySelector(".product-text-buy").addEventListener('click', function(event){
        let target = event.target;
        $.ajax({
            url: "/basket/add/" + target.name + "/",
            success: function(data){
                if (!data.result){
                    console.log('no')
                }else{
                    $('.basket-block').html(data.result);
                }
            },
        });
    event.preventDefault();
    });
}

// `use strict`
// window.onload = function () {
//     document.querySelector(".product-text-buy").addEventListener('click', function(event){
//         let target = event.target;
//         $.ajax({
//             url: "/basket/add/" + target.name + "/",
//             data: {'data': target.name},
//             contentType: 'application/json',
//             success: function(data){
//                 if (!data.result){
//                     console.log('no')
//                 }else{
//                     $('.basket-block').html(data.result);
//                 }
//             },
//         });
//     event.preventDefault();
//     });
// }