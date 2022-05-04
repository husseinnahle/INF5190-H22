function disable_fields() {
	var select = document.getElementById("select");
	var buttonRechercher = document.getElementById("button-rechercher");
	document.getElementById("inputArrondissement2").disabled = true;
	select.disabled = true;
	buttonRechercher.disabled = true;
	buttonRechercher.style.cursor = "not-allowed";
	select.style.cursor = "not-allowed";
}

function enable_fields() {
	var select = document.getElementById("select");
	var buttonRechercher = document.getElementById("button-rechercher");
	document.getElementById("inputArrondissement2").disabled = false;
	select.disabled = false;
	buttonRechercher.disabled = false;
	buttonRechercher.style.cursor = "pointer";
	select.style.cursor = "pointer";
}

function recherche_par_arrondissement() {
	reset_page();
	var arrondissement = document.getElementById("inputArrondissement2").value;
	if (arrondissement.length == 0) {
		document.getElementById("textHelp").innerHTML = "Ce champ ne peut pas etre vide!";
		return true;
	}
	document.getElementById("info").innerHTML = "Request in progress...";
	document.getElementById("textHelp").innerHTML = "";
	disable_fields();
	fetch('/api/installations?arrondissement=' + arrondissement)
		.then(function(response) {
			enable_fields();
			return response.text();
		}).then(function(text) {
			var jsonObject = JSON.parse(text);
			var output = "";
			for (var i = 0; i < jsonObject.length; i++) {
				output += `<tr><th scope="row">${jsonObject[i]["id"]}</th><td>${jsonObject[i]["nom"]}</td></tr>`;
			}
			document.getElementById("installation-tbody").innerHTML = output;
			document.getElementById("rechercher-resultat").style.visibility = "visible";
			document.getElementById("info").innerHTML = "";
			enable_fields();
		});
	return true;
}

function recherche_par_installation() {
	reset_page();
	document.getElementById("info").innerHTML = "Request in progress...";
	disable_fields();
	var installation = document.getElementById("select").value;
	installation.replaceAll(" ", "+");
	fetch('/api/installations?installation=' + installation)
		.then(function(response) {
			enable_fields();
			return response.text();
		}).then(function(text) {
			var jsonObject = JSON.parse(text);
			if (jsonObject["type"] == "piscine") {
				set_piscine_table(jsonObject);
			} else if (jsonObject["type"] == "patinoire") {
				set_patinoire_table(jsonObject);
			} else if (jsonObject["type"] == "glissade") {
				set_glissade_table(jsonObject);
			}
			document.getElementById("info").innerHTML = "";
			enable_fields();
		});
	return true;
}

function set_piscine_table(jsonObject) {
	document.getElementById("piscine").style.visibility = "visible";
	var output = `
    <tr>
      <th scope="row">${jsonObject["id"]}</th>
      <td>${jsonObject["id_uev"]}</td>
      <td>${jsonObject["type"]}</td>
      <td>${jsonObject["nom"]}</td>
      <td>${jsonObject["arrondissement"]}</td>
      <td>${jsonObject["adresse"]}</td>
      <td>${jsonObject["propriete"]}</td>
      <td>${jsonObject["gestion"]}</td>
      <td>${jsonObject["point_x"]}</td>
      <td>${jsonObject["point_y"]}</td>
      <td>${jsonObject["equipement"]}</td>
      <td>${jsonObject["long"]}</td>
      <td>${jsonObject["lat"]}</td>
    </tr>`;
	document.getElementById("piscine-tbody").innerHTML = output;
}

function set_glissade_table(jsonObject) {
	document.getElementById("glissade").style.visibility = "visible";
	var output = `
    <tr>
      <th scope="row">${jsonObject["id"]}</th>
      <td>${jsonObject["nom"]}</td>
      <td>${jsonObject["arrondissement"]}</td>
      <td>${jsonObject["cle"]}</td>
      <td>${jsonObject["date_maj"]}</td>
      <td>${jsonObject["ouvert"]}</td>
      <td>${jsonObject["deblaye"]}</td>
      <td>${jsonObject["condition"]}</td>
    </tr>`;
	document.getElementById("glissade-tbody").innerHTML = output;
}

function set_patinoire_table(jsonObject) {
	document.getElementById("patinoire").style.visibility = "visible";
	var output = `
      <tr>
      <th scope="row">${jsonObject["id"]}</th>
      <td>${jsonObject["nom"]}</td>
      <td>${jsonObject["arrondissement"]}</td>
      <td>
      <div class="conditions">
      <table class="table table-hover">
        <thead>
            <tr>
            <th scope="col">date_heure</th>
            <th scope="col">ouvert</th>
            <th scope="col">deblaye</th>
            <th scope="col">arrose</th>
            <th scope="col">resurface</th>
            </tr>
        </thead><tbody>`;
	for (var j = 0; j < jsonObject["conditions"].length; j++) {
		output += `
            <tr>
              <td>${jsonObject["conditions"][j]["date_heure"]}</td>
              <td>${jsonObject["conditions"][j]["ouvert"]}</td>
              <td>${jsonObject["conditions"][j]["deblaye"]}</td>
              <td>${jsonObject["conditions"][j]["arrose"]}</td>
              <td>${jsonObject["conditions"][j]["resurface"]}</td>
            </tr>`;
	}
	output += "</tbody></table></div></td>";
	document.getElementById("patinoire-tbody").innerHTML = output;
}

function reset_page() {
	document.getElementById("installation-tbody").innerHTML = "";
	document.getElementById("piscine-tbody").innerHTML = "";
	document.getElementById("patinoire-tbody").innerHTML = "";
	document.getElementById("glissade-tbody").innerHTML = "";
	document.getElementById("rechercher-resultat").style.visibility = "hidden";
	document.getElementById("piscine").style.visibility = "hidden";
	document.getElementById("patinoire").style.visibility = "hidden";
	document.getElementById("glissade").style.visibility = "hidden";
}