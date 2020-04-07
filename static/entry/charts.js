
const constCharts = {
    chartA: {
            chart: {
                type: 'bar',
                inverted: true,
            },
            title: {
                text: 'Fruit Consumption'
            },
            plotOptions: {
                series: {
                    stacking: 'normal'
                }
            },
            xAxis: {
                categories: ['Apples', 'Bananas', 'Oranges']
            },
            yAxis: {
                title: {
                    text: 'Fruit eaten'
                }
            },
            series: [{
                name: 'Jane',
                data: [1, 0, 4]
            }, {
                name: 'John',
                data: [5, 7, 3]
            }]
        },

    chartB: {
            chart: {
                type: 'bar',
                inverted: true,
            },
            title: {
                text: 'Fruit Consumption'
            },
            plotOptions: {
                series: {
                    stacking: undefined
                }
            },
            xAxis: {
                categories: ['Apples', 'Bananas', 'Oranges']
            },
            yAxis: {
                title: {
                    text: 'Fruit eaten'
                }
            },
            series: [{
                name: 'Jane',
                data: [1, 0, 4]
            }, {
                name: 'John',
                data: [5, 7, 3]
            }]
        }

};