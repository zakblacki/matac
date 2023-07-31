 
 
function getJSONData() {
    fetch('../static/js/Wilaya_Of_Algeria.json', {
        headers: {
          'Content-Type': 'application/json',
        },
      })
      .then(response => response.json())
      .then(jsonData => {
         
        for(data in jsonData){
            var wilaya = jsonData[data]
            
            document.getElementById("wilayaId").innerHTML += `<option value="${wilaya["id"]}" data-relai="600,00" data-home="900,00" data-id="1">${wilaya["name"]}</option>`
            // Do something with the JSON data here
        }
        
      })
      .catch(error => console.error("Error fetching JSON data.", error));
  }
  getJSONData()



  document.getElementById("wilayaId").addEventListener("click",function(){
     
    fetch('../static/js/Commune_Of_Algeria.json', {
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
            document.getElementById("Commune").innerHTML=""
            jsonData.filter((obj) =>{
              if( this.value == obj["wilaya_id"]){
                
                document.getElementById("Commune").innerHTML += `<option value="${obj["id"]}" data-relai="600,00" data-home="900,00" data-id="1">${obj["name"]}</option>`
              }
              
            });
            // Do something with the JSON data here
        // }
        
      })
      .catch(error => console.error("Error fetching JSON data.", error));
      
  })

