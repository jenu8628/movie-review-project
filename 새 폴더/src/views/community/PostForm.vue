<template>
  <div class="container text-center" style="width:50% ;margin-top : 10%">
    <div class="text-left my-3">Title</div>
    <div><input class="text-left btn btn-secondary" type="text" style="width:100%" v-model="Post.title"></div>
    <div class="text-left my-3">Content</div>
    <div><input class="text-left btn btn-secondary" type="text" style="width:100% ; height:100px;" v-model="Post.content"></div>
    <button class="btn btn-secondary my-3" @click="onPost">submit your review</button>
  </div>
</template>
<script>
import axios from 'axios'
const SERVER_URL = process.env.VUE_APP_SERVER_URL

export default {
  data : function () {
    return {
      Post : {
        content : '',
        title : '',
        username : localStorage.getItem('username')
      }
    }
  },
  methods : {
    setToken : function () {
      const token = localStorage.getItem('jwt')
      const config = {
        headers : {
          Authorization : `JWT ${token}`,
        }
      }
      return config
    },
    onPost : function () {
      axios.post(`${SERVER_URL}/community/post_list_create/`,this.Post,this.setToken())
      .then((res)=>{
        console.log(res)
        this.$router.push({name : "post_list"})
      })
      .catch((err)=>{
        console.log(err)
      })
    }
  }
}
</script>

<style>

</style>