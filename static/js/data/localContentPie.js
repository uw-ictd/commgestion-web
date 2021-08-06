Highcharts.chart("graph-4", {
  chart: {
    plotBackgroundColor: null,
    plotBorderWidth: null,
    plotShadow: false,
    type: "pie",
    animation: false,
  },
  title: {
    text: lookUpTitle("graph4"),
  },
  credits: {
    enabled: false,
  },
  tooltip: {
    pointFormat: "{point.percentage:.1f}%",
  },
  plotOptions: {
    pie: {
      allowPointSelect: true,
      cursor: "pointer",
      dataLabels: {
        enabled: true,
        format: "<b>{point.name}</b>: {point.percentage:.1f} %",
      },
    },
  },
  series: [
    {
      colorByPoint: true,
      data: lookUpData("graph4"),
    },
  ],
});
