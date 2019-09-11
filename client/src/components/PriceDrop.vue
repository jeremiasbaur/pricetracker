<template>
    <div class="card h-100 c">
      <img v-bind:src="pricedrops[2].url_image" class="card-img-top">
      <div class="mt-auto card-body d-flex flex-column">
        <h5 class="card-title">{{pricedrops[2].manufacturer}} {{pricedrops[2].name}}</h5>
        <p class="card-text percent">{{pricedrops[4].price}} CHF statt <del>{{pricedrops[3].price}} CHF</del><br>{{ -Math.round((pricedrops[0].percent_change-1)*1000)/10 }}% Rabatt!</p>
        <a v-bind:href="pricedrops[1].url" target="_blank" class="mt-auto btn btn-primary text-truncate">Deal anschauen!</a>
        <a v-bind:href="topPreise(pricedrops[2].manufacturer_id)" target="_blank" class="text-center text-secondary" style="padding: 0.2rem 0px 0px 0px;">Toppreise Vergleich</a>
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
