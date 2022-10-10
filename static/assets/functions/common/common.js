$('#transaction_type').on('change', function(element) {
    let selected_values = $('#transaction_type').val()
    if (selected_values.includes('CREDIT')) {
        $('#transaction_type').val(['CREDIT'])
        selected_values = $('#transaction_type').val()
    }
    // cash transaction
    let cashPaidElement =  $('#cash_paid_form_group')
    let balanceElement =  $('#balance_amount')
    if (selected_values.includes('CASH')) {
        cashPaidElement.show()
    } else {
        cashPaidElement.hide()
    }   

    let mpesaPaidElement =  $('#mpesa_paid_form_group')
    if (selected_values.includes('MPESA')) {
        mpesaPaidElement.show()
    } else {
        mpesaPaidElement.hide()
    } 

    if (selected_values.includes('CASH') || selected_values.includes('MPESA')) {
        balanceElement.show()
    } else { balanceElement.hide() }
});
  

$('#mpesa_paid').on('keyup change', function(element) {
    let mpesaPaid = element.target.value
    let totalPrice = $('#total_price').text()
    totalPrice = totalPrice - mpesaPaid
    cashPaid = $('#cash_paid').val()
    computeBalance(totalPrice, cashPaid)
 });


$('#cash_paid').on('keyup change', function(element) {
    let cashPaid = element.target.value
    let totalPrice = $('#total_price').text()
    const selected_values = $('#transaction_type').val()
    if (selected_values.includes('MPESA')) {
        mpesaPaid = $('#mpesa_paid').val()
        totalPrice = totalPrice - mpesaPaid
    }
    computeBalance(totalPrice, cashPaid)
 });


function computeBalance(totalPrice, cashAmount) {
    let balance = cashAmount - totalPrice
    let balanceElement =  $('#balance_amount')
    
    let childNodes = balanceElement.children().length
    if (childNodes == 1) {
        balanceElement.children("span:first").remove();
    }

    let textColor = 'grey';
    if (balance > 0) {
        textColor = 'green'
    } else if ( 0 > balance) {
        textColor = 'red'
    }

    $(
        `<span style="color: ${textColor};"> Balance: KES ${balance} </span>`
    ).appendTo('#balance_amount');

}
