function drawChart(data) {
   var svgWidth = 600, svgHeight = 400;
   var margin = { top: 20, right: 20, bottom: 30, left: 50 };
   var width = svgWidth - margin.left - margin.right;
   var height = svgHeight - margin.top - margin.bottom;
   var svg = d3.select('svg')
     .attr("width", svgWidth)
     .attr("height", svgHeight);
  var g = svg.append("g")
   .attr("transform", 
      "translate(" + margin.left + "," + margin.top + ")"
   );

  var x = d3.scaleTime().rangeRound([0, width]);
  var y = d3.scaleLinear().rangeRound([height, 0]);








