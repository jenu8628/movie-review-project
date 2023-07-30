<template>
  <div>
    <div class="container text-left d-flex" style="width:80%">
      <div class="col-9 ">
         <div>
          {{review.title}}
         </div>
         <div>
            <div class="blockquote mb-0">
              <h2>{{review.movie_title}}</h2>
              <p class="movie-content">{{review.content}}</p>
              <div style="font-size:1rem">
                 by {{review.username}} {{getStar(review.rank)}}<br>{{getCreatedAt(review)}} 
              </div>
            </div>
          </div>
          <div class="mt-5">
            <button class="btn btn-secondary ghost-button mr-3" style="border:solid;" @click="goDetail(review.id)">리뷰 더보기</button>
            <button class="btn btn-secondary ghost-button ml-3" style="border:solid;" @click="goMovieDetail(review.movie_title)">영화 정보</button>
          </div>
      </div>
      <div>
        <img :src="poster" alt="" style="width:100%">
      </div>
    </div>
    <hr style="width:80%;background-color: gray">
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
.movie-content {
  overflow: hidden;
text-overflow: ellipsis;
display: -webkit-box;
-webkit-line-clamp: 3;
-webkit-box-orient: vertical;
}
</style>