<template>
   <div>
    <PostForm />
    <router-view/>
  </div>
</template>

<script>
import PostForm from './PostForm.vue'

export default {
  components: {
    PostForm    
  },
}
</script>

<style>

</style>