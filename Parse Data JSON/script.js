var file = new FileReader();

function load() {
  file.readAsText(document.getElementById("inputfile").files[0]);
  file.onload = function() {
    convert();
  }
}

function convert() {
  try {
    var data = JSON.parse(file.result);
  } catch (e) {
    alert("JSON error \n\n" + e);
    return false;
  }

  var rows = Object.keys(data);
  var exportData = [];
  
  var session, utdid, variation_id;

  exportData.push(["Optimizely UUID", "Variation ID", "Timestamp", "UTD ID", "UTD Session ID", "Referrer URL"]);

  rows.forEach(function(item, index) {
    var attributes = data[item].attributes.list;

    attributes.forEach(function(item, index) {
      if (item.element.name == "visitor_sessionId") {
        session = item.element.value;
      }
    });

    attributes.forEach(function(item, index) {
      if (item.element.name == "visitor_userUtdId") {
        utdid = item.element.value;
      }
    });

    if (!!data[index].variation_id) {
      variation_id = data[index].variation_id;
    } else {
      var experiments = data[item].experiments.list;
      experiments.forEach(function(item, index) {
      if (!!item.element.variation_id) {
        variation_id = item.element.variation_id;
      }
    });
    }

    exportData.push([data[index].uuid, variation_id, data[index].timestamp, utdid, session, data[index].referer]);
  });

  var csv = "";

  exportData.forEach(function(row) {
    csv += row.join(',');
    csv += "\n";
  });

  var hiddenElement = document.createElement('a');
  hiddenElement.href = 'data:text/csv;charset=utf-8,' + encodeURI(csv);
  hiddenElement.target = '_blank';
  hiddenElement.download = 'converted.csv';
  hiddenElement.click();
}