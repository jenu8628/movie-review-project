<template>
  <div>
    <div class="container text-left d-flex" style="width:50%">
      <div class="col-9 ">
         <div>
          {{review.title}}
         </div>
         <div>
            <div class="blockquote mb-0">
              <h2>{{review.movie_title}}</h2>
              <p class="movie-content">{{review.content}}</p>
              <div style="font-size:1rem">
                {{getStar(review.rank)}} | {{getCreatedAt(review)}} 
              </div>
            </div>
          </div>
          <div class="mt-5">
            <button class="btn btn-secondary ghost-button mx-3" style="border:solid;" @click="goDetail(review.id)">상세보기</button>
            <button class="btn btn-secondary ghost-button mx-3" style="border:solid;" @click="goUpdate(review)">수정하기</button>
            <button  class="btn btn-secondary ghost-button mx-3" style="border:solid;" @click="onDelete(review.id)">삭제하기</button>
            <button class="btn btn-secondary ghost-button mx-3" style="border:solid;" @click="goMovieDetail(review.movie_title)">영화정보</button>

          </div>
      </div>
      <div>
        <img :src="poster" alt="" style="width:100%">
      </div>
    </div>
    <hr style="width:50%;background-color: gray">
  </div>
</template>

<script>
import moment from 'moment'
import movies from '../../movies.json'
import axios from 'axios'

const SERVER_URL = process.env.VUE_APP_SERVER_URL

export default {
  data () {
    return {
      movies : movies,
    } 
  },
  props : {
    review : [Array,Object,],
    poster : [String,Array,Object,]
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
      return moment(review.created_at).startOf('minute').fromNow()   
    },
    goDetail (reviewId) {
      window.location.href=`http://localhost:8080/community/movie_review_detail?review_id=${reviewId}`
    },
    getStar (rank) {
      let rankStar = '★'
      for (let i=1;i<rank;i++){
        rankStar += '★'
      }
      return rankStar
    },
    goUpdate : function (review) {
      console.log(review)
      this.$router.push({name : 'movie_review_update', params : {review :review}})
    },
    onDelete : function (id) {
      const config = this.setToken()
      axios.delete(`${SERVER_URL}/community/movie_review_update_delete/${id}/`,config)
      .then(()=>{
      window.location.href=`http://localhost:8080/community/community_mypage`
      })
      .catch((err)=>{
        console.log(err)
      })
    },
    goMovieDetail (movieTitle) {
      window.location.href=`http://localhost:8080/movie_detail?movie_title=${movieTitle}`
    }
  }
}
</script>

<style>

</style>