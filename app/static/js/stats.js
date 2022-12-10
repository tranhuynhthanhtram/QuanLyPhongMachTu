function billChart(labels, data){
    const ctx = document.getElementById('billMonthChart');

    new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: labels,
      datasets: [{
        label: 'Doanh thu',
        data: data,
        borderWidth: 1,
        backgroundColor: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange', 'Black' , 'Pink', 'Brown', 'White', 'Gray', 'Lavender']
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
}

function mediChart(labels, data){
    const ctx = document.getElementById('mediChart');

    new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [{
        label: 'Số lần dùng',
        data: data,
        borderWidth: 1,
        backgroundColor: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange', 'Black' , 'Pink', 'Brown', 'White', 'Gray', 'Lavender']
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
}