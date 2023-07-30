<template>
  <div class="container text-left" style="margin-top:10%">
    <div style="min-height:70vh;">
      <span v-if="me === review.username">
        <button class="btn btn-secondary ghost-button" @click="goUpdate(review)">수정하기</button>
        <button  class="btn btn-secondary ghost-button" @click="onDelete(review.id)">삭제하기</button>
      </span>
      <h1> {{review.title}} </h1>
      <h2> {{review.content}} </h2>

      <div class="m-3"><PostLike :review_id="review_id"/></div>
      <PostCommentForm :review_id="review_id"/>
      <PostComment :review_id="review_id"/>
    </div>

    <div><PostList /></div>
  </div>
</template>

<script>
import axios from 'axios'
import PostLike from './PostLike.vue'
import PostComment from './PostComment.vue'
import PostList from './PostList.vue'
import PostCommentForm from './PostCommentForm.vue'

const SERVER_URL = process.env.VUE_APP_SERVER_URL

export default {
  data : function () {
    return {
      review_id : this.$route.query.review_id,
      update_delete : false,
      username : '',
      review : '',
      me : localStorage.getItem('username')
    }
  },
  components : {
    PostLike,
    PostComment,
    PostCommentForm,
    PostList,
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
    goBack : function () {
      this.$router.push({name : 'post_list'})
    },
    goUpdate : function (review) {
      this.$router.push({name : 'post_update', params : {review :review}})
    },
    onDelete : function (id) {
      const config = this.setToken()
      axios.delete(`${SERVER_URL}/community/post_update_delete/${id}/`,config)
      .then(()=>{
        this.$router.push({name : 'post_list'})
      })
      .catch((err)=>{
        console.log(err)
      })
    }
  },
  created : function () {
    const config = this.setToken()
    axios.get(`${SERVER_URL}/community/get_user_posts/${this.review_id}/`,config)
    .then((res)=>{
      this.review = {
        title  : res.data.title,
        content : res.data.content,
        id : res.data.id,
        username : res.data.username,
      }
      this.username = res.data.username
      if(res.data.is_review_user){
        this.update_delete = true
      }
    })
  }
}
</script>

<style>

</style>