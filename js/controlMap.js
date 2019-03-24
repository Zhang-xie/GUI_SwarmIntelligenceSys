var myChart = echarts.init(document.getElementById('mainControlMap'));  
var data1 = [];
var data2 = [];
var data3 = [];

// var errorWidth = 30;
// var windowWidth = myChart.width = window.innerWidth - errorWidth,
//     windowHeight = myChart.height = window.innerHeight - errorWidth;

var random = function (max) {
  return (Math.random() * max).toFixed(3);
};

for (var i = 0; i < 50; i++) {
  data1.push([random(15), random(10), random(1)]);
  data2.push([random(10), random(10), random(1)]);
  data3.push([random(15), random(10), random(1)]);
}

option = {
  animation: false,
  // legend: {
  //  data: ['scatter', 'scatter2', 'scatter3']
  // },
  tooltip: {
  },
  xAxis: {
    show: false,
    type: 'value',
    min: 'dataMin',
    max: 'dataMax',
    splitLine: {
      show: false
    }
  },
  yAxis: {
    show: false,
    type: 'value',
    min: 'dataMin',
    max: 'dataMax',
    splitLine: {
      show: false
    }
  },
  dataZoom: [
    {
      type: 'slider',
      show: true,
      xAxisIndex: [0],
      start: 1,
      end: 35
    },
    {
      type: 'slider',
      show: true,
      yAxisIndex: [0],
      left: '93%',
      start: 29,
      end: 36
    },
    {
      type: 'inside',
      xAxisIndex: [0],
      start: 1,
      end: 35
    },
    {
      type: 'inside',
      yAxisIndex: [0],
      start: 29,
      end: 36
    }
  ],
  series: [
    {
      name: 'scatter',
      type: 'scatter',
      itemStyle: {
        normal: {
          opacity: 0.8
        }
      },
      symbolSize: function (val) {
        return val[2] * 40;
      },
      data: data1
    },
    {
      name: 'scatter2',
      type: 'scatter',
      itemStyle: {
        normal: {
          opacity: 0.8
        }
      },
      symbolSize: function (val) {
        return val[2] * 40;
      },
      data: data2
    },
    {
      name: 'scatter3',
      type: 'scatter',
      itemStyle: {
        normal: {
          opacity: 0.8,
        }
      },
      symbolSize: function (val) {
        return val[2] * 40;
      },
      data: data3
    }
  ]
}

// 使用刚指定的配置项和数据显示图表。
myChart.setOption(option);