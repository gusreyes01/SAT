$(document).ready(function () {
		    $("[rel=tooltip]").tooltip();
		    $('#tabbed-widget a').click(function (e) {
				e.preventDefault();
				$(this).tab('show');
			});
			$('.table-data').dataTable();

	        //var myvalues = [10,8,5,7,4,4,1];
	        //$('.dynamicsparkline').sparkline(myvalues);

	        $('.inlinebar').sparkline('html', {
	        	type: 'bar', 
	        	barColor: '#468847',
	        	lineWidth: 1,
	        	height: "20px",
	        });
	        $('.inlineline').sparkline('html', {
	        	type: 'line', 
	        	barColor: '#468847',
	        	lineWidth: 1,
	        	height: "20px",
	        	lineColor: '#82b721',
			    fillColor: '#fff',
			    width:"50px",
	        });
	        $(".small-chart .inlineline").sparkline([5,6,7,9,9,5,3,2,0,4,6,7], {
			    type: 'line',
			    width: '150px',
			    height: '100px',
			    lineColor: '#82b721',
			    fillColor: '#538115',
			    lineWidth: 5,
			    spotColor: '#95c535',
			    minSpotColor: '#95c535',
			    maxSpotColor: '#95c535',
			    highlightSpotColor: '#333',
			    highlightLineColor: '#000',
			    spotRadius: 6,
			    normalRangeColor: '#111',
			    drawNormalOnTop: false
			});

	        $(".small-chart .inlinebar").sparkline([5,6,7,2,0,-4,-2,-6], {
			    type: 'bar',
			    height: '100',
			    barColor: '#4fa950',
			    negBarColor: '#ce483d',
			    stackedBarColor: '#FFA93C',
			    barWidth: 10,
			    barSpacing: 3,
			    nullColor: '#aaa'
			});
			$('.small-chart .inlinestackbar').sparkline([ [1,4], [2,2], [2, 4], [5, 2], [3, 5], [4, 1] ], { type: 'bar',
			    height: '100',
			    barWidth: 10,
			    barSpacing: 3,
			    stackedBarColor: ['#00aced','#ce483d','#FFA93C','#4fa950']
			});

			$(".small-chart .inlinepie").sparkline([1,1,2,5], {
			    type: 'pie',
			    width: '100px',
			    height: '100px',
			    sliceColors: ['#00aced','#ce483d','#FFA93C','#4fa950'],
			    offset: 0
			});
			
			var colors = [ "#008A17", "#0072C6",  "#FFA93C", "#AC193D"];
			$.plot(
				$("#flot-example-1"),
					[
						{ label: "Green", data: [ [0, 1], [1, 14], [2, 5], [3, 4], [4, 5], [5, 1], [6, 14], [7, 5], [8, 5] ] },
						{ label: "Blue", data: [ [0, 5], [1, 2], [2, 10], [3, 1], [4, 9],  [5, 5], [6, 2], [7, 10], [8, 8]  ] },
					], {
				    xaxis: {
						font: {
						    color: "#ccc",
						    size: 11,
						}
					},
					yaxis: {
						font: {
						    color: "#ccc",
						    size: 11,
						}
					},
				    series: {
						lines: { 
							show: true,
							lineWidth: 5,
							fill: .5,
						},
						points: { 
							show: true,
							radius: 0,
						},
					},
					grid: {
						clickable: true,
					    hoverable: true,
					    autoHighlight: true,
					    mouseActiveRadius: 10,
					    aboveData: true,
					    backgroundColor: "#fff",
					    borderWidth: 0,
					    minBorderMargin: 25,
					},
					colors: colors,
				    shadowSize: 0,
				}
			);
			$.plot(
				$("#flot-example-2"),
				[
					{
						label: "Total Things Per Year",
						data: [ [2011, 450], [2012, 550], [2013, 320], [2014, 700], [2015, 1200], [2016, 300], [2017, 800] ],
						bars: {
							show: true,
							lineWidth: 3,
							barWidth: 0.5,
							align: "center"
						},
					}
				],
				{
					xaxis: {
						ticks: [
							[2011, "2011"],
							[2012, "2012"],
							[2013, "2013"],
							[2014, "2014"],
							[2015, "2015"],
							[2016, "2016"],
							[2017, "2017"],
						]
					},
					grid: {
						clickable: true,
					    hoverable: true,
					    autoHighlight: true,
					    mouseActiveRadius: 10,
					    aboveData: true,
					    backgroundColor: "#fff",
					    borderWidth: 0,
					    minBorderMargin: 25,
					},
					colors: colors,
				}
			);
			$.plot(
				$("#flot-example-3"),
				[
					{
						label: "This",
						data: 44	
					},
					{
						label: "That",
						data: 75
					},
					{
						label: "The Other Thing",
						data: 22
					}
				],
				{
					series: {
						pie: {
							show: true,
							label: {
								show: true
							}
						}
					},
					colors: colors,
				} 
			);
		  });