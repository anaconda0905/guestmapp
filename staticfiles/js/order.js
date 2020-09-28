$("#modal_form_order_step2 button[type='submit']").on('click', function(event){
    event.preventDefault();
    if (cardFormValidate()) {
        var productType = $('#modal_form_order_step2 #product_type').find(":selected").val();
        var metadata = ""
        var tires = $('#modal_form_order_step2 input[name="tires"]').val();
        var price = $("#modal_form_order_step2 .price").text();
        var card_name = $("#modal_form_order_step2 input[name='cardname']").val()
        var card_number = $("#modal_form_order_step2 input[name='cardnumber']").val()
        var cvv = $("#modal_form_order_step2 input[name='cvv']").val()
        var expiry_date = $("#modal_form_order_step2 input[name='expiry_date']").val()
        $("#modal_form_order_step2 button[type='submit']").attr('disabled', 'disabled');
        $("#modal_form_order_step2 button[type='submit'] .loader").css('display', 'block');
        $.ajax({
            url: '/payout/',
            method: 'POST',
            data: {
                productType: productType,
                metadata:metadata,
                tires:tires,
                price:price,
                card_name:card_name,
                card_number:card_number,
                cvv:cvv,
                expiry_date:expiry_date,
                csrfmiddlewaretoken:$('#modal_form_order_step2 input[name=csrfmiddlewaretoken]').val(),
            },
            success:function(response){
                if(response.success){
                $("#modal_form_order_step2 button[type='submit']").removeAttr('disabled');
                $('#modal_form_order_step2').modal('hide');
                $('#modal_form_order_complete').modal('show');
                $("#modal_form_order_step2 button[type='submit'] .loader").css('display', 'none');
                var price = response.data.price / 100;
                $("#modal_form_order_complete .price").text('$' + price);
                }
                else{
                //set active pay button
                $("#modal_form_order_step2 button[type='submit']").removeAttr('disabled');
                $('#modal_form_order_step2 #msg-btn').html(response.message + '&times');
                $('#modal_form_order_step2 #alert-div').addClass('active');
                //hide progress view
                $("#modal_form_order_step2 button[type='submit'] .loader").css('display', 'none');
                }
                //reset all input field of order modal
                $('#modal_form_order_step2 input[name="tires"]').val('');
                $("#modal_form_order_step2 input[name='cardname']").val('');
                $("#modal_form_order_step2 input[name='cardnumber']").val('');
                $("#modal_form_order_step2 input[name='cvv']").val('');
                $("#modal_form_order_step2 input[name='expiry_date']").val('');
                $('#modal_form_order_step2 .currency-unit').removeClass('active');
                $('#modal_form_order_step2 .price').text('');
                $('#modal_form_order_step2 .totalPrice').text('');
            },
        });
    } 
});

$('#modal_form_order_step2 #msg-btn').on('click', function(event){
    $('#modal_form_order_step2 #alert-div').removeClass('active');
});

function cardFormValidate(){
    var cardValid = 0;

    //card number validation
    $('#card_number').validateCreditCard(function(result){
        if(result.valid){
            $("#card_number").removeClass('required');
            cardValid = 1;
        }else{
            $("#card_number").addClass('required');
            cardValid = 0;
        }
    });
      
    //card details validation
    var cardName = $("#name_on_card").val();
    var expiry_date = $("#expiry_date").val();
    var cvv = $("#cvv").val();
    var regName = /^[a-z ,.'-]+$/i;
    var regDate = /\b(0[1-9]|1[0-2])\/?([0-9]{4}|[0-9]{2})\b/;
    var regCVV = /^[0-9]{3,3}$/;
    if (cardValid == 0) {
        $("#card_number").addClass('required');
        $("#card_number").focus();
        return false;
    }else if (!regDate.test(expiry_date)) {
        $("#card_number").removeClass('required');
        $("#expiry_date").addClass('required');
        $("#expiry_date").focus();
        return false;
    }else if (!regCVV.test(cvv)) {
        $("#card_number").removeClass('required');
        $("#expiry_date").removeClass('required');
        $("#cvv").addClass('required');
        $("#cvv").focus();
        return false;
    }else if (!regName.test(cardName)) {
        $("#card_number").removeClass('required');
        $("#expiry_date").removeClass('required');
        $("#cvv").removeClass('required');
        $("#name_on_card").addClass('required');
        $("#name_on_card").focus();
        return false;
    }else{
        $("#card_number").removeClass('required');
        $("#expiry_date").removeClass('required');
        $("#cvv").removeClass('required');
        $("#name_on_card").removeClass('required');
        return true;
    }
}