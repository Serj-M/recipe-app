<template>
  <v-app>
    <v-app-bar
      color="white"
      dark
    >
        <div class="d-flex align-center">
          <p class="name_app"></p>
          <v-spacer></v-spacer>
          <router-link to='/' class="mr-2">
            <v-btn text>
              <span>Recipes</span>
            </v-btn>
          </router-link>
    
          <router-link to="/about">
            <v-btn text>
              <span>About me</span>
            </v-btn>
          </router-link>
        </div>
  
    </v-app-bar>

    <v-content>
      <div class="wrap">
        <router-view />
      </div>
    </v-content>
  </v-app>
</template>

<script setup>
</script>

<style scoped>
.name_app {
  font-size: 25px;
  padding-left: 40px;
}
.wrap {
  margin-top: 50px;
}
</style>
