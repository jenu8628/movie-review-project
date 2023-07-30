<template>
  <div>
    <div class="d-flex " v-for="(comment,idx) in comments" :key="idx">
      <h4 class="align-self-center mr-3">
        {{comment.username}} 
      </h4>
      <h4 class="align-self-center">
        {{comment.content}}
      </h4>
      <button class="btn btn-secondary ghost-button" style="font-size : 30px" v-if="me==comment.username" @click="deleteComment(comment.id)">x</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
const SERVER_URL = process.env.VUE_APP_SERVER_URL

export default {
  data : function () {
    return {
      comments : [],
      me : localStorage.getItem('username')
    }
  },
  props : {
    review_id : [String,Number],
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
    getComments : function () {
      const config = this.setToken()
      axios.get(`${SERVER_URL}/community/get_post_comments/${this.review_id}/`,config)
      .then((res)=>{
        this.comments = res.data
      })
    },
    deleteComment : function (comment_id) {
      const config = this.setToken()
      axios.delete(`${SERVER_URL}/community/movie_review_comment_delete/${comment_id}/`,config)
      .then(()=>{
        this.$router.go(this.$router.currentRoute)
      })      
    }
  },
  created : function () {
    this.getComments()
  }
}
</script>

<style>

</style>