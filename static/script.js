BASE_URL = 'http://127.0.0.1:5000/api';

function generateCupcake(cupcake) {
	return `<div data-id=${cupcake.id}> <li>${cupcake.flavor} / ${cupcake.size} / ${cupcake.rating}<button class="delete-button">X</button> </li> <img src="${cupcake.image}" alt="No image available" class="cupcake-image"> </div>`;
}

async function showCupcakes() {
	const res = await axios.get(`${BASE_URL}/cupcakes`);

	for (let cupcakeData of res.data.cupcakes) {
		cupcake = $(generateCupcake(cupcakeData));
		$('#cupcake-list').append(cupcake);
	}
}

$('#cupcake-form').on('submit', async function(evt) {
	evt.preventDefault();

	flavor = $('#flavor').val();
	size = $('#size').val();
	rating = $('#rating').val();
	image = $('#image').val();

	// if (image === None) {
	// 	image = 'https://tinyurl.com/demo-cupcake';
	// }

	const res = await axios.post(`${BASE_URL}/cupcakes`, {
		flavor,
		size,
		rating,
		image
	});

	let newCupcake = $(generateCupcake(res.data.cupcake));
	$('#cupcake-list').append(newCupcake);
	$('#cupcake-form').trigger('reset');
});

$('#cupcake-list').on('click', '.delete-button', async function(evt) {
	let $cupcake = $(evt.target).closest('div');
	let id = $cupcake.attr('data-id');

	await axios.delete(`${BASE_URL}/cupcakes/${id}`);

	$cupcake.remove();
});

$(showCupcakes);
