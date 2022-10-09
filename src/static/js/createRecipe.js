function htmlToElement(html) {
	var template = document.createElement('template');
	html = html.trim(); // Never return a text node of whitespace as the result
	template.innerHTML = html;
	return template.content.firstChild;
}

function selectIngredient(name, id) {
	document.getElementById(id).remove();

	// Create the element
	let html = `
	<div class="ingredient">
		<p>${name}</p>
		<input type="text" class="ingredientInput" name="quantity" placeholder="Määrä"/>
		<input type="text" class="ingredientInput" name="unit" placeholder="Yksikkö"/>
	</div>
	`;
	let element = htmlToElement(html);

	document.getElementById('selectedIngredients').appendChild(element);
}
