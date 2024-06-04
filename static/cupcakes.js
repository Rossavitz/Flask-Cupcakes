const BASE_API_URL = "http://127.0.0.1:5000/api";

function showCupcakeHomePage(cupcake) {
  return `
    <div cupcake-id=${cupcake.id}>
    <li>Flavor:
    ${cupcake.flavor} - Size:${cupcake.size} - Rating:${cupcake.rating}
    <button class="delete-cupcake">Delete</button>
    </li>
    <img class="cupcake-img", src="${cupcake.image}"
    </div>`;
}

async function showCupcakes() {
  const response = await axios.get(`${BASE_API_URL}/cupcakes`);

  for (let data of response.data.cupcakes) {
    let newCupcake = $(showCupcakeHomePage(data));
    $("cupcake-list").append(newCupcake);
    console.log(response.data.cupcakes);
  }
}

$("#add-cupcake-form").on("submit", async function (e) {
  e.preventDefault();
  let flavor = $("#flavor-form").val();
  let size = $("#size-form").val();
  let rating = $("#rating-form").val();
  let image = $("#image-form").val();

  const response = await axios.post(`${BASE_API_URL}/cupcakes`, {
    flavor,
    size,
    rating,
    image,
  });

  let newCupcake = $(showCupcakeHomePage(response.data.cupcake));
  $("#cupcake-list").append(newCupcake);
  $("#add-cupcake-form").trigger("reset");
});

$("#cupcake-list").on("click", ".delete-button", async function (e) {
  let $cupcake = $(e.target).closest("div");
  let id = $cupcake.attr("cupcake-id");

  await axios.delete(`${BASE_URL}/cupcakes/${id}`);
  $cupcake.remove();
});

$(showCupcakeHomePage);
