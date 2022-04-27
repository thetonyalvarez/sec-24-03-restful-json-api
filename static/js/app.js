const $newCupcakeForm = $("#new-cupcake-form")
const $cupcakeList = $("#cupcake-list")

const BASE_URL = 'http://127.0.0.1:5000/api'

const config = {
    header: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin' : "*",
        "Access-Control-Allow-Methods": "*",
        "Access-Control-Allow-Headers": "'Access-Control-Allow-Headers: Origin, Content-Type, X-Auth-Token'",
    }
}

const generateCupcakeHTML = (cupcake) => {
    return `
        <li class="col-6 col-sm-4 col-lg-3">
            <div class="card">
                <img class="card-img-top" src=${cupcake.image} alt="${ cupcake.flavor }"/>
                <div class="card-body">
                    <div class="badge badge-secondary">${ cupcake.size }</div>
                    <h2>${ cupcake.flavor }</h2>
                    <p>Rating: ${ cupcake.rating }</p>
                </div>
            </div>
        </li>
    `
}

const get_all_cupcakes = async () => {
    console.debug("get_all_cupcakes")

    const resp = await axios({
        'method': 'GET',
        'url': `${BASE_URL}/cupcakes`,
        config
    })

    let { cupcakes } = resp.data

    for (let cupcake of cupcakes) {
        let new_cupcake = $(generateCupcakeHTML(cupcake))
        $cupcakeList.append(new_cupcake)
    }
}

const create_cupcake = async (e) => {
    console.debug("create_cupcake", create_cupcake)
    e.preventDefault();

    let flavor = $("#flavor").val();
    let size = $("#size").val();
    let rating = $("#rating").val();
    let image = $("#image").val();

    const resp = await axios.post(`${BASE_URL}/cupcakes`, {
        flavor, size, rating, image
    })

    let {cupcake} = resp.data

    console.log(cupcake, '!!!')

    let newCupcake = $(generateCupcakeHTML(cupcake))
    $cupcakeList.append(newCupcake)
    $newCupcakeForm.trigger("reset")

}

$newCupcakeForm.on('submit', create_cupcake)

$(get_all_cupcakes)