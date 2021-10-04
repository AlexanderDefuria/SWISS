
const constCharts = {

    templateChart: {
            chart: {
                type: 'bar',
                inverted: true,
            },
            title: {
                text: 'Match Data'
            },
            plotOptions: {
                series: {
                    stacking: undefined
                }
            },
            xAxis: {
                categories: ['Team 4343', 'Team 914']
            },
            yAxis: {
                title: {
                    text: 'Balls Scored'
                }
            },
            series: [{
                name: 'Match 1',
                data: [3, 4]
            }, {
                name: 'Match 2',
                data: [5, 7]
            }]
        },

    totalChart: {
            chart: {
				backgroundColor: '#0F4D8D',
             style: {
                    color: '#ffffff'
                    }
			},
            title: {
                text: 'Total Balls Scored Over Comp',
                style: {
                    color: '#ffffff'
                }
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
                data: [0]
            }],
            xAxis: {
                title: {
                    text: 'Match',
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
                },            responsive: {
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
            tooltip: {
                valueDecimals: 3,
            },
            series: [{
                name: 'Lower',
                data: [0, 0]
            }, {
                name: 'Outer',
                data: [0, 0]
            }, {
                name: 'Inner',
                data: [0, 0]
            }]
    }


};

