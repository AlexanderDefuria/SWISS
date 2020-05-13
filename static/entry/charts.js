
const constCharts = {

    templateChart: {
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
        },

    totalChart: {
            chart: {
				backgroundColor: '#dddddd'
			},
            title: {
			    text: 'Total Balls Scored Over Comp'
            },

            plotOptions: {
                series: {
                    label: {
                        connectorAllowed: true
                    },
                    pointStart: 1
                }
                },
            series: [{
                name: 'Balls Scored',
                data: [10, 15, 20, 17, 25, 10, 13, 22]
            }],
            responsive: {
                rules: [{
                    condition: {
                        maxWidth: 500
                    },
                    chartOptions: {
                        legend: {
                            layout: 'horizontal',
                            align: 'center',
                            verticalAlign: 'bottom'
                        }
                    }
                }]
            }
    },

    avgChart: {
            chart: {
                backgroundColor: '#0F4D8D',
                type: 'bar',
                style: {
                    color: '#ffffff'
                    }
                    },
            title: {
                text: 'Average Balls Scored Per Match',
                style: {
                    color: '#ffffff'
                }
                },
            xAxis: {
                categories: ['Auto', 'Teleop'],
                labels: {
                    style: {
                        color: '#ffffff'
                    }
                }
                },
            yAxis: {
                title: {
                    text: 'Balls Scored',
                    style: {
                        color: '#ffffff'
                    }
                    },
                labels: {
                    style: {
                        color: '#ffffff'
                    }
                }
                },
            series: [{
                name: 'Lower',
                data: [0, 0]
            }, {
                name: 'Outer',
                data: [3, 20]
            }, {
                name: 'Inner',
                data: [2, 5,]
            }]
    }


};

