eel.expose(addText);
function addText(text, statusCode){
	let ul = document.getElementById('userRepos');
	let p = document.createElement('p');
	p.innerHTML = (`
		<p><strong>Error, Unexpected Behaviour !!!. Status Code: ${statusCode}</p>
		<p><strong> Message: ${text}</p>
	`);
	ul.appendChild(p);
}

eel.expose(addWaitMsg);
function addWaitMsg(){
	let ul = document.getElementById('userRepos');
	let p = document.createElement('p');
	p.id = 'msg';
	p.innerHTML = (`
		<p><strong>Plz Wait, Fetching Results !!!!</p>
	`);
	ul.appendChild(p);
}

eel.expose(removeWaitMsg);
function removeWaitMsg(){
	let p = document.getElementById('msg');
	p.innerHTML = "";
}

function RepoOfOrganisztion() {
	var organisationName = document.getElementById('usernameInput').value;
	var topRepositoriesCount = document.getElementById('topRepoInput').value;
	var topContributersCount = document.getElementById('topComitteInput').value;
	topRepositoriesCount = parseInt(topRepositoriesCount);
	topContributersCount = parseInt(topContributersCount);
	let root = document.getElementById('userRepos');
	while (root.firstChild) {
		root.removeChild(root.firstChild);
	}
	console.log("called");
	eel.fetchReposOfOrganisationsAndContibutors(organisationName, topRepositoriesCount, topContributersCount)(function(ret){
		console.log(ret)
		let ul = document.getElementById('userRepos');
		let p = document.createElement('p');
		p.innerHTML = (`<p><strong>Number of Public Repos:${topRepositoriesCount}</p>`)
		ul.appendChild(p);
		for(let i in ret[0]){
			let li = document.createElement('li');
			li.classList.add('list-group-item')
			li.innerHTML = (`
			<p><strong>Repo:</strong> <a href="${ret[0][i][3]}">${ret[0][i][1]}</a></p>
			<p><strong>Description:</strong> ${ret[0][i][2]}</p>
			<p><strong>Fork Count:</strong> ${ret[0][i][0]}</p>
		`);
			li.innerHTML += `<p><strong>Number of Top Contributers:</strong> ${ret[1][i].length}</p>`;
			for(j in ret[1][i]){
				li.innerHTML += `<p>Name: </strong><a href="${ret[1][i][j][2]}">${ret[1][i][j][0]}</a></p>`;
				li.innerHTML += `<p>Contibutions: </strong> ${ret[1][i][j][1]}</p>`;
			}
			ul.appendChild(li);
		}
	})
}
