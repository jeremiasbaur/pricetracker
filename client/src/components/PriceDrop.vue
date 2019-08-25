<template>
    <div class="col-md-4 box mx-auto">
        <div class="card c">
          <img v-bind:src="pricedrops[2].url_image" class="card-img-top">
          <div class="card-body">
            <h5 class="card-title">{{pricedrops[2].manufacturer}} {{pricedrops[2].name}}</h5>
              <p class="card-text percent">64.30 CHF statt <del>100 CHF</del><br>{{ -Math.round((pricedrops[0].percent_change-1)*1000)/10 }}% Rabatt!</p>
            <a v-bind:href="pricedrops[1].url" target="_blank" class="btn btn-primary">Deal anschauen!</a>
          </div>
        </div>
      </div>
</template>

<script>
export default {
  name: 'PriceDrop',
  // To use props, they must be declared
  props: {
    pricedrops: Array,
  }
}
</script>

<style>
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
  float: none;
  box-shadow: 0 0 16px 10px rgba(0, 0, 0, 0.1);
  width: 22rem;
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
