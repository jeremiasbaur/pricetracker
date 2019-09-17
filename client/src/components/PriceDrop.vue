<template>
    <div class="card h-100 c">
      <img v-bind:src="pricedrops.product_url_image" class="card-img-top">
      <div class="mt-auto card-body d-flex flex-column">
        <h5 class="card-title">{{pricedrops.product_manufacturer}} {{pricedrops.product_name}}</h5>
        <p class="card-text percent">{{pricedrops.price_today}} CHF statt <del>{{pricedrops.price_yesterday}} CHF</del><br>{{ -Math.round((pricedrops.percent_change-1)*1000)/10 }}% Rabatt!</p>
        <a v-bind:href="pricedrops.product_company_url" target="_blank" class="mt-auto btn btn-primary text-truncate">PriceDrop anschauen!</a>
        <a v-bind:href="topPreise(pricedrops.product_tag)" target="_blank" class="text-center text-secondary" style="padding: 0.2rem 0px 0px 0px;">Toppreise Vergleich</a>
      </div>
    </div>
</template>

<script>
export default {
  name: 'PriceDrop',
  // To use props, they must be declared
  props: {
    pricedrops: Array,
  },
  methods: {
    topPreise(manufacturer_id){
        return "https://www.toppreise.ch/produktsuche?q=" + manufacturer_id.replace(" ", "+");
        // f'https://www.toppreise.ch/produktsuche?q={str(product.product.manufacturer_id).replace(" ", "+")}'
    }
  }
}
</script>

<style>
.card-body {
    padding: 1.25rem 1.25rem 0px 1.25rem;
}

.percent {
    color:green;
}

.box {
padding: 20px;
}

.c {
  padding: 15px;
  //margin-top: 30px;
  margin: 0 auto;
  //float: none;
  box-shadow: 0 0 16px 10px rgba(0, 0, 0, 0.1);
  //width: 22rem;
}

.c img {
  object-fit: contain;
  border-radius: 5px;
  background-color: white;
  box-shadow: 0 1px 10px 5px rgba(0, 0, 0, 0.09);
  padding:10px;
  //max-width:100%;
  height:250px;
}
</style>
