<template>
  <div class="container">
    <center><h1 id="text06">PriceDrop.ch</h1></center>
      <hr width="50%">
    <div class="row">
      <div v-for="(price, index) in prices" :key="index" class="col-lg-4 col-md-6 mt-3">
      <PriceDrop v-bind:pricedrops="price"></PriceDrop>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import Alert from './Alert.vue';
import PriceDrop from './PriceDrop.vue';

export default {
  data() {
    return {
      prices: [],
      addBookForm: {
        title: '',
        author: '',
        read: [],
      },
      message: '',
      showMessage: false,
    };
  },
  components: {
    alert: Alert,
    PriceDrop
  },
  methods: {
    getPrices() {
      const path = '/prices';
      axios.get(path)
        .then((res) => {
          console.log(res);
          this.prices = res.data.prices;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    }
  },
  created() {
    this.getPrices();
  },
};
</script>

