<template>
  <main role="main" class="container">
    <div id="app">
      <router-view/>
    </div>
  </main>
</template>

<style>
@import url('https://fonts.googleapis.com/css?family=Nunito&display=swap');
html, body{
  //background-image: linear-gradient(180deg, #1C1F4D 23%, #4B3870 100%);
  font-family: 'Nunito', sans-serif;
  //color: #FFFFFF;
}
#app {
  margin-top: 5vmin;
  display: block;
  margin-right: auto;
  margin-left: auto;
}

#text06 {
    //color: #FFFFFF;
    font-family: 'Nunito', sans-serif;
    letter-spacing: 0.15rem;
    width: calc(100% + 0.15rem);
    font-size: 6vmax;
    line-height: 1.25;
    font-weight: 700;
}

</style>
