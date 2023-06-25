// function getNewValue() {
//   var uinew = document.getElementsByName("uinew");
//   // console.log(uinew.length)
//   // for(var i=0;i<2.length;i++) {
//   Array.from(uinew, (e) => {
//     console.log("HI");
//     if (uinew[i].checked) {
//       console.log(uinew.value);
//       return uinew.value;
//     }
//   });
// }

function getNewValue() {
  var uinew = document.getElementsByName("uinew");
  for (var i in uinew) {
    if (uinew[i].checked) {
      return parseInt(i);
    }
  }
  return -1;
}

function getGymValue() {
  var uigym = document.getElementsByName("uigym");
  for (var i in uigym) {
    if (uigym[i].checked) {
      return parseInt(i);
    }
  }
  return -1;
}

function getLiftValue() {
  var uilift = document.getElementsByName("uilift");
  for (var i in uilift) {
    if (uilift[i].checked) {
      return parseInt(i);
    }
  }
  return -1;
}


function getClubValue() {
  var uiclub = document.getElementsByName("uiclub");
  for (var i in uiclub) {
    if (uiclub[i].checked) {
      return parseInt(i);
    }
  }
  return -1; 
}

function getCarValue() {
  var uicar= document.getElementsByName("uicar");
  for (var i in uicar) {
    if (uicar[i].checked) {
      return parseInt(i);
    }
  }
  return -1; 
}

function getGasValue() {
  var uigas = document.getElementsByName("uigas");
  for (var i in uigas) {
    if (uigas[i].checked) {
      return parseInt(i);
    }
  }
  return -1;
}

function getTrackValue() {
  var uitrack = document.getElementsByName("uitrack");
  for (var i in uitrack) {
    if (uitrack[i].checked) {
      return parseInt(i);
    }
  }
  return -1;
}

function getPoolValue() {
  var uipool = document.getElementsByName("uipool");
  for (var i in uipool) {
    if (uipool[i].checked) {
      return parseInt(i);
    }
  }
  return -1;
}

function getBHKValue() {
  var uiBHK = document.getElementsByName("uiBHK");
  for (var i in uiBHK) {
    if (uiBHK[i].checked) {
      return parseInt(i) + 1;
    }
  }
  return -1;
}

function onClickedEstimatePrice() {
  console.log("Estimate price button clicked");
  var area = document.getElementById("uiarea").value;
  console.log(area)
  var bhk = getBHKValue();
  var New = getNewValue();
  var gym = getGymValue();
  var lift = getLiftValue();
  var club = getClubValue();
  var car = getCarValue();
  var gas = getGasValue();
  var track = getTrackValue();
  var pool = getPoolValue();
  var location = document.getElementById("uiLocations").value;
  console.log(location)
  
  var estPrice = document.getElementById("uiEstimatedPrice");

  var formdata = new FormData();
formdata.append("Area", area);
formdata.append("Location", location);
formdata.append("bhk", bhk);
formdata.append("New_or_Resale", New);
formdata.append("Gymnasium", gym);
formdata.append("Lift_Available", lift);
formdata.append("Car_Parking", car);
formdata.append("Clubhouse", club);
formdata.append("Gas_Connection", gas);
formdata.append("Jogging_Track", track);
formdata.append("Swimming_Pool", pool);

console.log({
    area: parseFloat(area),
    bhk: bhk,
    new: New,
    gym: gym,
    lift: lift,
    club: club,
    car: car,
    gas: gas,
    track: track,
    pool: pool,
    location: location,
  });
var requestOptions = {
  method: 'POST',
  body: formdata,
  redirect: 'follow'
};

fetch("http://127.0.0.1:5000/predict_home_price", requestOptions)
  .then(response => response.text())
  .then(result => {
    console.log(result)
    estPrice.innerHTML = "<h2>" + JSON.parse(result)["estimated_price"] + "</h2>"})
  .catch(error => console.log('error', error));
}
function onPageLoad() {
  console.log("document loaded");
  var url = "http://127.0.0.1:5000/get_location_names";
  $.get(url, function (data, status) {
    console.log("got response for get_location_names request");
    if (data) {
      var locations = data.locations;
      var uiLocations = document.getElementById("uiLocations");
      $("#uiLocations").empty();
      for (var i in locations) {
        var opt = new Option(locations[i]);
        $("#uiLocations").append(opt);
      }
    }
  });
}

window.onload = onPageLoad;
console.log(getNewValue());
