const last30daysperiodnames = JSON.parse(document.getElementById('last30daysperiodnames').textContent);
const last30daysvalues = JSON.parse(document.getElementById('last30daysvalues').textContent);
var ctx = document.getElementById('chart_last30daysevents').getContext('2d');
Chart.defaults.color = '#ffffff';
Chart.defaults.font.family = '-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,"Noto Sans",sans-serif,"Apple Color Emoji","Segoe UI Emoji","Segoe UI Symbol","Noto Color Emoji"';
Chart.defaults.font.size = 16;

var chart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: last30daysperiodnames,
        datasets: [{
            label: 'Statechanges per day',
            backgroundColor: '#00798a',
            fill: true,
            borderColor: '#01C696',
            data: last30daysvalues,
            pointBorderColor: '#01C696',
            pointBackgroundColor: '#ffffff',
            fontColor: '#ffffff',
        }]
    },

    // Configuration options go here
    options: {
        maintainAspectRatio: false,
        responsive: true,
        tooltips: {
            mode: 'index',
            intersect: false,
        },
        hover: {
            mode: 'nearest',
            intersect: true
        },
        scales: {
            xAxes: [{
                type: 'time',
                time: {
                    format: 'DD/MM/YYYY',
                    unit: 'day'
                },
                display: true,
                scaleLabel: {
                    display: true,
                    labelString: 'Last 30 days',
                    padding: 1
                }
            }]
        }

    }
});
