function GenerateChart() {
    var BarCharturl = 'http://127.0.0.1:5000/GetCarStatsByYear'

    google.charts.load('current', {
        packages: ['corechart']
      }).then(function () {
        $.ajax({
          url: BarCharturl,
          dataType: 'json'
        }).done(function (jsonData) {
          var data = new google.visualization.DataTable();
          data.addColumn('number', 'year');
          data.addColumn('string', 'make');
          data.addColumn('string', 'model');
          data.addColumn('number', 'count');
      
          $.each(jsonData, function (index, row) {
            data.addRow([
              row.year,
              row.make,
              row.model,
              row.count
            ]);
            console.log(row);
          });
                
          var chart = new google.visualization.PieChart(document.getElementById('barChartDiv'));
          chart.draw(data, {width: 400, height: 240});
        });
      });
};