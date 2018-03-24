

importdata = data



function return_data(){


    x = {
        labels: ["January", "February", "March", "April", "May", "June", "July"],
        datasets: [{
            label: "Insight",
            backgroundColor: [],
            borderColor: 'rgb(255, 255, 255)',
            data: [3, 10, 5, 2, 20, 30, 45],
        }]
    }

    x.labels = importdata.category
    x.datasets[0].data = importdata.score
     for (var i = x.labels.length - 1; i >= 0; i--) {
         x.datasets[0].backgroundColor[x.datasets[0].backgroundColor.length]= getRandomColor();
      }


    return x;
}




var ctx = document.getElementById('myChart').getContext('2d');




var chart = new Chart(ctx, {
    // The type of chart we want to create
    type: 'pie',

    // The data for our dataset
    data: return_data(),

    // Configuration options go here
    options: {responsive: true}
});




document.getElementById("myChart").onclick = function(evt)
{   
    var activePoints = chart.getElementsAtEvent(evt);

    if(activePoints.length > 0)
    {
      //get the internal index of slice in pie chart
      var clickedElementindex = activePoints[0]["_index"];

      //get specific label by index 
      var labelw = chart.data.labels[clickedElementindex];

      //get value by index      
      var value = chart.data.datasets[0].data[clickedElementindex];

      clickedonchart(labelw)

      /* other stuff that requires slice's label and value */
   }
}

function clickedonchart(label){


}


function getRandomColor() {
  var letters = '0123456789ABCDEF';
  var color = '#';
  for (var i = 0; i < 6; i++) {
    color += letters[Math.floor(Math.random() * 16)] ;
  }
  return color;
}


authorizationToken = 'Access-Control-Allow-Headers'
function setRandomColor() {
  $("#colorpad").css("background-color", getRandomColor());
}



searchthis = "science"


// $.ajax({
//         type: 'POST',
//         headers : {'Access-Control-Allow-Origin': 'x-requested-with'},
//         url: "http://localhost:8080/pythoncodes.py",
//         data: {//"json=" + escape(JSON.stringify(createRequestObject)
//         //param: searchthis http://localhost:8000/
//         }, //passing some input here
//         success: function(response){
//            output = response;
//            alert(output);
//         }
// }).done(
// );

//$.post('http://localhost:8080', {file_url: 'pythoncodes.py'}, function(d){console.log(d)})







