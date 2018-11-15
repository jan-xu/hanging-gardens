var ul = $('ul#side-menu');

$.ajax({
  url : '/static/extend_dashboard_links.html',
  type: "get",
  success : function(response) {
    console.log("Load /static/extend_dashboard_links.html");
    ul.append(response);
  }
});

var wrapper = $('div#wrapper');
$.ajax({
  url : '/static/extend_dashboard_pages.html',
  type: "get",
  success : function(response){
      console.log("Load /static/extend_dashboard_pages.html");
      wrapper.append(response);
  }
});

// Add function to get points for report page
function getPoints( the_network_id, the_object_id, the_stream_id, callback ){
  var query_data = {};
  var query_string = '?'+$.param(query_data);
  var url = '/networks/'+the_network_id+'/objects/'+the_object_id;
  url += '/streams/'+the_stream_id+'/points'+query_string;

  // Send the request to the server
  $.ajax({
    url : url,
    type: "get",
    success : function(response){
      console.log( response );

      if( response['points-code'] == 200 ){
        var num_points = response.points.length
        var most_recent_value = response.points[0].value
        console.log("Most recent value: "+most_recent_value);
        console.log("Number of points retrieved: "+num_points);
        callback( response.points );
      }
    },
    error : function(jqXHR, textStatus, errorThrown){
      console.log(jqXHR);
    }
  });
}

// Call getPoints if Input or Report is selected
// ...added feature to dynamically update plot as new data becomes available
custom_sidebar_link_callback = function( select ){
  if (select == 'illuminance'){
    var plotCalls = 0;
    var plotTimer = setInterval( function(){
      getPoints('local','light_sensor','center_light', function(points){
        console.log( "The points request was successful!" );
        illuminance_loadPlot( points );
      });
      if( plotCalls > 20 ){
        console.log( 'Clear timer' );
        clearInterval( plotTimer );
      }else{
        plotCalls += 1;
      }
    }, 1000);
  } else if (select == 'exposure'){
    var plotCalls = 0;
    var plotTimer = setInterval( function(){
      getPoints('local','exposure','exposure', function(points){
        console.log( "The points request was successful!" );
        exposure_loadPlot( points );
      });
      if( plotCalls > 20 ){
        console.log( 'Clear timer' );
        clearInterval( plotTimer );
      }else{
        plotCalls += 1;
      }
    }, 1000);
  } else if (select == 'temperature'){
    var plotCalls = 0;
    var plotTimer = setInterval( function(){
      getPoints('local','thermometer','temperature', function(points){
        console.log( "The points request was successful!" );
        temperature_loadPlot( points );
      });
      if( plotCalls > 20 ){
        console.log( 'Clear timer' );
        clearInterval( plotTimer );
      }else{
        plotCalls += 1;
      }
    }, 1000);
  } else if (select == 'energy'){
    var plotCalls = 0;
    var plotTimer = setInterval( function(){
      getPoints('local','energy','total_energy', function(points){
        console.log( "The points request was successful!" );
        energy_loadPlot( points );
      });
      if( plotCalls > 20 ){
        console.log( 'Clear timer' );
        clearInterval( plotTimer );
      }else{
        plotCalls += 1;
      }
    }, 1000);
  }
}

// Function to plot data points using Highcharts
function illuminance_loadPlot( points ){
  var plot = $('#content-illuminance');
  // Check if plot has a Highcharts element
  if( plot.highcharts() === undefined ){
    // Create a Highcharts element
    plot.highcharts( illuminance_plot_options );
  }

  // Iterate over points to place in Highcharts format
  var datapoints = [];
  for ( var i = 0; i < points.length; i++){
    var at_date = new Date(points[i].at);
    var at = at_date.getTime() - at_date.getTimezoneOffset()*60*1000;
    datapoints.unshift( [ at, points[i].value] );
  }

  // Update Highcharts plot
  if( plot.highcharts().series.length > 0 ){
    plot.highcharts().series[0].setData( datapoints );
  }else{
    plot.highcharts().addSeries({
      name: "Illuminance [lux]",
      data: datapoints
    });
  }
}

function exposure_loadPlot( points ){
  var plot = $('#content-exposure');
  // Check if plot has a Highcharts element
  if( plot.highcharts() === undefined ){
    // Create a Highcharts element
    plot.highcharts( exposure_plot_options );
  }

  // Iterate over points to place in Highcharts format
  var datapoints = [];
  for ( var i = 0; i < points.length; i++){
    var at_date = new Date(points[i].at);
    var at = at_date.getTime() - at_date.getTimezoneOffset()*60*1000;
    datapoints.unshift( [ at, points[i].value] );
  }

  // Update Highcharts plot
  if( plot.highcharts().series.length > 0 ){
    plot.highcharts().series[0].setData( datapoints );
  }else{
    plot.highcharts().addSeries({
      name: "Exposure [lux*s]",
      data: datapoints
    });
  }
}

function temperature_loadPlot( points ){
  var plot = $('#content-temperature');
  // Check if plot has a Highcharts element
  if( plot.highcharts() === undefined ){
    // Create a Highcharts element
    plot.highcharts( temperature_plot_options );
  }

  // Iterate over points to place in Highcharts format
  var datapoints = [];
  for ( var i = 0; i < points.length; i++){
    var at_date = new Date(points[i].at);
    var at = at_date.getTime() - at_date.getTimezoneOffset()*60*1000;
    datapoints.unshift( [ at, points[i].value] );
  }

  // Update Highcharts plot
  if( plot.highcharts().series.length > 0 ){
    plot.highcharts().series[0].setData( datapoints );
  }else{
    plot.highcharts().addSeries({
      name: "Temperature [°C]",
      data: datapoints
    });
  }
}

function energy_loadPlot( points ){
  var plot = $('#content-energy');
  // Check if plot has a Highcharts element
  if( plot.highcharts() === undefined ){
    // Create a Highcharts element
    plot.highcharts( energy_plot_options );
  }

  // Iterate over points to place in Highcharts format
  var datapoints = [];
  for ( var i = 0; i < points.length; i++){
    var at_date = new Date(points[i].at);
    var at = at_date.getTime() - at_date.getTimezoneOffset()*60*1000;
    datapoints.unshift( [ at, points[i].value] );
  }

  // Update Highcharts plot
  if( plot.highcharts().series.length > 0 ){
    plot.highcharts().series[0].setData( datapoints );
  }else{
    plot.highcharts().addSeries({
      name: "Total energy consumption [kWh]",
      data: datapoints
    });
  }
}

var illuminance_plot_options = {
  chart: {
    type: 'line'
  },
  xAxis: {
    type: 'datetime',
    dateTimeLabelFormats: { // don't display the dummy year
      month: '%e. %b',
      year: '%b'
    },
  },
  title: {
    text: 'Illuminance received by plants [lux]'
  },
};

var exposure_plot_options = {
  chart: {
    type: 'line'
  },
  xAxis: {
    type: 'datetime',
    dateTimeLabelFormats: { // don't display the dummy year
      month: '%e. %b',
      year: '%b'
    },
  },
  title: {
    text: 'Daily exposure received by plants [lux*s]'
  },
};

var temperature_plot_options = {
  chart: {
    type: 'line'
  },
  xAxis: {
    type: 'datetime',
    dateTimeLabelFormats: { // don't display the dummy year
      month: '%e. %b',
      year: '%b'
    },
  },
  title: {
    text: 'Temperature [°C]'
  },
};

var energy_plot_options = {
  chart: {
    type: 'line'
  },
  xAxis: {
    type: 'datetime',
    dateTimeLabelFormats: { // don't display the dummy year
      month: '%e. %b',
      year: '%b'
    },
  },
  title: {
    text: 'Total energy consumption [kWh]'
  },
};
