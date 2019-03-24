/* <script type="text/javascript"> */
			// 基于准备好的dom，初始化echarts实例
			var myChart = echarts.init(document.getElementById('main'));
			/*myChart.setOption({
				series : [
					{
						name: '访问来源',
						type: 'pie',
						radius: '55%',
						data:[
							{value:235, name:'视频广告'}, 
							{value:274, name:'联盟广告'},
							{value:310, name:'邮件营销'},
							{value:335, name:'直接访问'},
							{value:400, name:'搜索引擎'}
						],
						roseType: 'angle',
						itemStyle: {
							normal: {
								shadowBlur: 200,
								shadowColor: 'rgba(0, 0, 0, 0.5)'
							}
						}
					}
				]
			})*/
			// 指定图表的配置项和数据
		   /* var option = {
				title: {
					text: 'ECharts 入门示例'
				},
				tooltip: {},
				legend: {
					data:['销量']
				},
				xAxis: {
					data: ["衬衫","羊毛衫","雪纺衫","裤子","高跟鞋","袜子"]
				},
				yAxis: {},
				series: [{
					name: '销量',
					type: 'bar',
					data: [5, 20, 36, 10, 10, 20]
				}]
			};*/
			
			var data1 = [];
			var data2 = [];
			var data3 = [];

			var random = function (max) {
				return (Math.random() * max).toFixed(3);
			};

			for (var i = 0; i < 500; i++) {
				data1.push([random(15), random(10), random(1)]);
				data2.push([random(10), random(10), random(1)]);
				data3.push([random(15), random(10), random(1)]);
			}

			option = {
				animation: false,
				// legend: {
				// 	data: ['scatter', 'scatter2', 'scatter3']
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
			
/* 		</script> */