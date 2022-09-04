let lineChartCanvases = $('.line-chart').get()

lineChartCanvases.forEach((chartCanvasItem) => {

    let areaChartCanvas = chartCanvasItem.getContext('2d')
    fetchedLabels = JSON.parse(chartCanvasItem.getAttribute('label'))
    fetchedData = JSON.parse(chartCanvasItem.getAttribute('data'))

    chartConfig = [
      {
        label               : '',
        backgroundColor     : 'rgba(60,141,188,0.9)',
        borderColor         : 'rgba(60,141,188,0.8)',
        pointRadius          : false,
        pointColor          : '#3b8bba',
        pointStrokeColor    : 'rgba(60,141,188,1)',
        pointHighlightFill  : '#fff',
        pointHighlightStroke: 'rgba(60,141,188,1)',
        data                : null,
        fill                : false
      },
      {
        label               : '',
        backgroundColor     : 'rgba(0, 179, 89, 1)',
        borderColor         : 'rgba(0, 179, 89, 1)',
        pointRadius         : false,
        pointColor          : 'rgba(0, 179, 89, 1)',
        pointStrokeColor    : '#00b359',
        pointHighlightFill  : '#fff',
        pointHighlightStroke: 'rgba(220,220,220,1)',
        data                : null,
        fill                : false
      },
      {
        label               : '',
        backgroundColor     : 'rgba(232, 232, 48, 1)',
        borderColor         : 'rgba(232, 232, 48, 1)',
        pointRadius         : false,
        pointColor          : 'rgba(232, 232, 48, 1)',
        pointStrokeColor    : '#e8e830',
        pointHighlightFill  : '#fff',
        pointHighlightStroke: 'rgba(220,220,220,1)',
        data                : null,
        fill                : false
      },
      {
        label               : '',
        backgroundColor     : 'rgba(255, 77, 77, 1)',
        borderColor         : 'rgba(255, 77, 77, 1)',
        pointRadius         : false,
        pointColor          : 'rgba(255, 77, 77, 1)',
        pointStrokeColor    : '#ff4d4d',
        pointHighlightFill  : '#fff',
        pointHighlightStroke: 'rgba(220,220,220,1)',
        data                : null,
        fill                : false
      }
    ]

    let dataset = []
    fetchedData.forEach((item, index) => {
      if(chartConfig[index]) {
          let datasetObject = chartConfig[index]
          datasetObject.label = item.label
          datasetObject.data = item.data
          dataset.push(datasetObject)
      }
    })

    var chartData = {
      labels  : fetchedLabels,
      datasets: dataset
    }

    var chartOptions = {
      maintainAspectRatio : false,
      responsive : true,
      legend: {
        display: true
      },
      scales: {
        xAxes: [{
          gridLines : {
            display : false,
          }
        }],
        yAxes: [{
          gridLines : {
            display : false,
          }
        }]
      }
    }

    // This will get the first returned node in the jQuery collection.
    new Chart(areaChartCanvas, {
      type: 'line',
      data: chartData,
      options: chartOptions
    })

})










