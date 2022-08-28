//Date range as a button
$('#daterange-btn').daterangepicker(
    {
        ranges   : {
        'Today'       : [moment(), moment()],
        'Yesterday'   : [moment().subtract(1, 'days'), moment().subtract(1, 'days')],
        'Last 7 Days' : [moment().subtract(6, 'days'), moment()],
        'Last 30 Days': [moment().subtract(29, 'days'), moment()],
        'This Month'  : [moment().startOf('month'), moment().endOf('month')],
        'Last Month'  : [moment().subtract(1, 'month').startOf('month'), moment().subtract(1, 'month').endOf('month')],
        'Last 3 Months'  : [moment().subtract(3, 'month').startOf('month'), moment().subtract(1, 'month').endOf('month')],
        'Last 6 Months'  : [moment().subtract(6, 'month').startOf('month'), moment().subtract(1, 'month').endOf('month')],
        'This Year'  : [moment().startOf('year'), moment().subtract(1, 'month').endOf('month')],
        'Last 1 Year'  : [moment().subtract(12, 'month').startOf('month'), moment().subtract(1, 'month').endOf('month')]
        },
        startDate: moment().subtract(29, 'days'),
        endDate  : moment()
    },
    function (start, end) {
        $('#daterange-input').val(start.format('D, M, YYYY') + ' - ' + end.format('D, M, YYYY'))
    }
)
  