<template>
  <div>
    <MovieReviewForm />
    <router-view/>
  </div>
</template>

<script>
import MovieReviewForm from './MovieReviewForm.vue'

export default {
  components: {
    MovieReviewForm    
  },
}
</script>

<style>

</style>