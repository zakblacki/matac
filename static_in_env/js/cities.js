 
 
function getJSONData() {
    fetch('/static/js/Wilaya_Of_Algeria.json', {
        headers: {
          'Content-Type': 'application/json',
        },
      })
      .then(response => response.json())
      .then(jsonData => {
         
        for(data in jsonData){
            var wilaya = jsonData[data]
            
            document.getElementById("wilayaId").innerHTML += `<option data-valu="${wilaya['name']}" value="${wilaya["id"]}" data-relai="600,00" data-home="900,00" data-id="1">${wilaya["name"]}</option>`
            // Do something with the JSON data here
        }
        
      })
      .catch(error => console.log("Error fetching JSON data."));
  }



  document.addEventListener("DOMContentLoaded", function() {
  getJSONData()



  document.getElementById("wilayaId").addEventListener("click",function(e){
     
    fetch('/static/js/Commune_Of_Algeria.json', {
        headers: {
          'Content-Type': 'application/json',
        },
      })
      .then(response => response.json())
      .then(jsonData => {
         
        // const filteredArray = jsonData.filter((obj) => obj["wilaya_id"] = 1);
        // console.log(filteredArray);
        // for(data in jsonData){
        //     var comun = jsonData[data]
            // const filteredArray = myArray.filter((obj) => obj.age > 30);
            // console.log(comun["wilaya_id"]);
            //  
            const selectedWilayaId = e.target.value; // Assuming wilayaId is the clicked element
            document.getElementById("Commune").innerHTML=""
            jsonData.filter((obj) =>{
              if (selectedWilayaId == obj["wilaya_id"]) {
                document.getElementById("Commune").innerHTML += `<option data-valu="${obj['name']}" value="${obj["id"]}" data-relai="600,00" data-home="900,00" data-id="1">${obj["name"]}</option>`;
            }
              
            });
            // Do something with the JSON data here
        // }
        
      })
      .catch(error => console.log("Error fetching JSON data."));
      
  })


})