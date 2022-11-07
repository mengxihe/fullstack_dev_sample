<template>
  <router-view></router-view>
</template>

<script setup>
import { RouterView} from 'vue-router';
import {useRoute, useRouter} from "vue-router"
// get route info.
let route = useRoute()
// instance router
let router = useRouter()
</script>


