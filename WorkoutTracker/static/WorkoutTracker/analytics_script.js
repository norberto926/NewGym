
  const ctx = document.getElementById('myChart');

  const data = document.currentScript.dataset;
  const dataset = data.dataset;
  console.log(dataset)

  new Chart(ctx, {
    type: 'line',
    data: {
      labels:[],
      datasets: [{
        label: '# of Votes',
        data: [],
        borderWidth: 3
      }]
    },
    options: {
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  });
  const dateFilterButton = document.getElementsByClassName('date-filter')[0]

    const dateFiltering = async () => {
      const dateFrom = document.getElementById('date_from').value
      const dateTo = document.getElementById('date_to').value
      const response = await fetch(`/date_filter/?date_from=${dateFrom}&date_to=${dateTo}`)
      const data = await response.json()

  }
  dateFilterButton.addEventListener('click', dateFiltering)


