let pieChartCanvases = $('.pie-chart').get()

pieChartCanvases.forEach((chartCanvasItem) => {

    let chartCanvas = chartCanvasItem.getContext('2d')
    fetchedLabels = JSON.parse(chartCanvasItem.getAttribute('label'))
    fetchedData = JSON.parse(chartCanvasItem.getAttribute('data'))


    var chartData = {
      labels  : fetchedLabels,
      datasets: fetchedData
    }

    var chartOptions = {
      maintainAspectRatio : false,
      responsive : true,
    }

    new Chart(chartCanvas, {
      type: 'pie',
      data: chartData,
      options: chartOptions
    })

})
 