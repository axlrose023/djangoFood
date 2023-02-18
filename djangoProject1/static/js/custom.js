let autocomplete;

function initAutoComplete() {
    autocomplete = new google.maps.places.Autocomplete(
        document.getElementById('id_address'),
        {
            types: ['geocode', 'establishment'],
            componentRestrictions: {'country': ['ua']},
        })
    autocomplete.addEventListener('place_changed', onPlaceChanged);
}

function onPlaceChanged() {
    var place = autocomplete.getPlace();
    if (!place.geometry) {
        document.getElementById('id_address').placeholder = "Start typing..."
    } else {
        console.log('place name=>', place.name)
    }
}

$(document).ready(function () {
    $('.add_to_cart').on('click', function (e) {
        e.preventDefault();
        food_id = $(this).attr('data-id');
        url = $(this).attr('data-url');

        $.ajax({
            type: 'GET',
            url: url,
            success: function (response) {
                console.log(response)
                if (response.status == 'login_required') {
                    swal(response.message, '', 'info').then(function () {
                        window.location = '/accounts/login/';
                    })
                } else if (response.status == 'Failed') {
                    swal(response.message, '', 'error')
                } else {
                    $('#cart_counter').html(response.cart_counter["cart_count"]);
                    $('#qty-' + food_id).html(response.qty);
                    //subtotal, tax and grand total
                    applyCartAmount(
                        response.cart_amount['subtotal'],
                        response.cart_amount['tax_dict'],
                        response.cart_amount['grand_total'],
                    )
                }
            }
        });
    });
    $('.item_qty').each(function () {
        var the_id = $(this).attr('id')
        var qty = $(this).attr('data-qty')
        $('#' + the_id).html(qty)
    })
    $('.decrease_cart').on('click', function (e) {
        e.preventDefault();
        food_id = $(this).attr('data-id');
        url = $(this).attr('data-url');
        cart_id = $(this).attr('id');
        $.ajax({
            type: 'GET',
            url: url,
            success: function (response) {
                console.log(response)
                if (response.status == 'login_required') {
                    swal(response.message, '', 'info').then(function () {
                        window.location = '/accounts/login/';
                    })
                } else if (response.status == 'Failed') {
                    swal(response.message, '', 'error')
                } else {
                    $('#cart_counter').html(response.cart_counter["cart_count"]);
                    $('#qty-' + food_id).html(response.qty);
                    removeCartItem(response.qty, cart_id);
                    applyCartAmount(
                        response.cart_amount['subtotal'],
                        response.cart_amount['tax_dict'],
                        response.cart_amount['grand_total'],
                    )
                }
            }
        })
    })
    //Delete cart item
    $('.delete_cart').on('click', function (e) {
        e.preventDefault();
        cart_id = $(this).attr('data-id');
        url = $(this).attr('data-url');
        $.ajax({
            type: 'GET',
            url: url,
            success: function (response) {
                console.log(response)
                if (response.status == 'Failed') {
                    swal(response.message, '', 'error')
                } else {
                    $('#cart_counter').html(response.cart_counter["cart_count"]);
                    swal(response.status, response.message, 'success')
                    removeCartItem(0, cart_id);
                    checkEmptyCart();
                }
            }
        })
    })

    function removeCartItem(cartItemQty, cart_id) {
        if (cartItemQty <= 0) {
            document.getElementById("cart-item-" + cart_id).remove()
        }
    }

    function checkEmptyCart() {
        var cart_counter = document.getElementById('cart_counter').innerHTML
        if (cart_counter == 0) {
            document.getElementById("empty-cart").style.display = 'block'
        }
    }

    function applyCartAmount(subtotal, tax_dict, grand_total) {
        if (window.location.pathname == '/cart/') {
            $('#subtotal').html(subtotal)
            $('#total').html(grand_total)
            console.log(tax_dict)
            for (key1 in tax_dict) {
                console.log(tax_dict[key1])
                for (key2 in tax_dict[key1]) {
                    console.log(tax_dict[key1][key2])
                    $('#tax-' + key1).html(tax_dict[key1][key2])
                }
            }
        }

    }

    $('#add_hour').on('click', function (e) {
        e.preventDefault();
        var day = document.getElementById('id_day')
        var from_hour = document.getElementById('id_from_hour').value
        var to_hour = document.getElementById('id_to_hour').value
        var is_closed = document.getElementById('id_is_closed').checked
        var csrf_token = $('input[name=csrfmiddlewaretoken]').val()
        var url = document.getElementById('add_hour_url').value
        console.log(day, from_hour, to_hour, is_closed, csrf_token, url);
        if (is_closed) {
            is_closed = 'True'
            condition = "day != ''"

        } else {
            is_closed = 'False'
            condition = "day != '' && from_hour != '' && to_hour != ''"
        }
        if (eval(condition)) {
            $.ajax({
                type: 'POST',
                url: url,
                data: {
                    'day': day,
                    'from_hour': from_hour,
                    'to_hour': to_hour,
                    'is_closed': is_closed,
                    'csrfmiddlewaretoken': csrf_token,
                },
                success: function (response) {
                    console.log(response)
                }
            })
            console.log('add the entry')
        } else {
            swal("Please fill the fields", '', 'info')
        }
    })
});
// Render the PayPal button into #paypal-button-container
