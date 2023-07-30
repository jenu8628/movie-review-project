<template>
  <div class="container text-left" style="margin-top:3%">
  <div style="min-height:95vh;">
    <span v-if="update_delete">
      <button class="btn btn-secondary ghost-button" @click="goUpdate(review)">수정하기</button>
      <button  class="btn btn-secondary ghost-button" @click="onDelete(review.id)">삭제하기</button>
    </span>
    <h1> {{review.title}} </h1>
    <h2> {{review.movie_title}} : {{rankStar}}</h2> 
    <h2>{{review.content}}</h2>
    <div class="blockquote mb-0">
      <div style="font-size:1rem">
          by {{review.username}} <br>{{getCreatedAt(review)}} 
      </div>
    </div>
    <div class="m-3"><MovieReviewLike :review_id="review_id"/></div>
    <MovieReviewCommentForm :review_id="review_id"/>
    <MovieReviewComment :review_id="review_id"/>
  </div>



    <div><MovieReviewList/></div>
  </div>
</template>

<script>
import axios from 'axios'
import MovieReviewLike from './MovieReviewLike.vue'
import MovieReviewComment from './MovieReviewComment.vue'
import MovieReviewCommentForm from './MovieReviewCommentForm.vue'
import MovieReviewList from './MovieReviewList.vue'
import moment from 'moment'


const SERVER_URL = process.env.VUE_APP_SERVER_URL

export default {
  data : function () {
    return {
      review_id : this.$route.query.review_id,
      update_delete : false,
      username : '',
      review : '',
      rankStar : '★',
    }
  },
  components : {
    MovieReviewLike,
    MovieReviewComment,
    MovieReviewCommentForm,
    MovieReviewList,
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
    getCreatedAt : function (review) {
      console.log(review.created_at)
      return moment(review.created_at).startOf('minute').fromNow()   
    },
    goBack : function () {
      this.$router.push({name : 'movie_review_list'})
    },
    goUpdate : function (review) {
      this.$router.push({name : 'movie_review_update', params : {review :review}})
    },
    onDelete : function (id) {
      const config = this.setToken()
      axios.delete(`${SERVER_URL}/community/movie_review_update_delete/${id}/`,config)
      .then(()=>{
        this.$router.push({name : 'movie_review_list'})
      })
      .catch((err)=>{
        console.log(err)
      })
    }
  },
  created : function () {
    const config = this.setToken()
    axios.get(`${SERVER_URL}/community/get_user_movie_reviews/${this.review_id}/`,config)
    .then((res)=>{
      this.review = {
        title  : res.data.title,
        content : res.data.content,
        rank : res.data.rank,
        movie_title : res.data.movie_title,
        id : res.data.id,
        username : res.data.username,
        created_at : res.data.created_at,
      }
      for (let i = 1;i <res.data.rank;i++){
        this.rankStar = this.rankStar + '★'
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