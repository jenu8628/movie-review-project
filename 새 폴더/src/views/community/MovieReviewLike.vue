<template>
  <div class="d-flex justify-content-center">
    <button class="btn btn-secondary dislike-button" style="font-size : 30px" v-if="isLikeUser" @click="onClickLike(review_id)">Dislike</button>
    <button class="btn btn-secondary like-button" style="font-size : 30px" v-else @click="onClickLike(review_id)">Like</button>
    <span class="align-self-center" style="font-size : 30px">{{likeUsers}}</span>
  </div>
</template>

<script>
import axios from 'axios'

const SERVER_URL = process.env.VUE_APP_SERVER_URL

export default {
  data : function () {
    return {
      isLikeUser : false,
      likeUsers : 0,
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
    onClickLike : function (review_id) {
      const config = this.setToken()
      axios.post(`${SERVER_URL}/community/like_movie_review/${review_id}/`, review_id, config)
      .then((res)=>{
        this.isLikeUser = res.data.is_like_user
        this.likeUsers = res.data.like_users
      })
      .catch((err)=>{
        console.log(err)
      })
    },
    getLikeUser : function () {
      const config = this.setToken()
      axios.get(`${SERVER_URL}/community/like_movie_review/${this.review_id}`, config)
      .then((res)=>{
        this.isLikeUser = res.data.is_like_user
        this.likeUsers = res.data.like_users
      })
    }
  },
  created : function () {
    this.getLikeUser()
  }
}
</script>

<style>
.like-button {
  min-width: 10%;
  border: none;
}
.dislike-button {
  min-width: 10%;
  border: none;
}
</style>