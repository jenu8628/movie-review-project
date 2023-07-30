<template>
  <div v-if="reviews.length" class="list-box">
    <div class="col-12" style="min-height:30vh" v-for="(review,idx) in reviews" :key="idx">
        <MypageList :poster="getPoster(review.movie_title)" :review="review"/>
    </div>
  </div>
  <div v-else class="list-box">
    게시물이 아직 없습니다!
  </div>
</template>

<script>
import axios from 'axios'
import MypageList from './MypageList.vue'
import movies from '../../movies.json'

const SERVER_URL = process.env.VUE_APP_SERVER_URL

export default {
  data () {
    return {
      reviews : [],
      movies : movies,
      
    }
  },
  components : {
    MypageList
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
    getMy () {
      const config = this.setToken()
      axios.get(`${SERVER_URL}/community/get_user_reviews/`,config)
      .then((res)=>{
        this.reviews = res.data
        console.log(this.reviews)
      })
    },
    getPoster (movieTitle) {
      const movie = this.movies.find((movie)=>{
        return movie.title === movieTitle
      })
      return movie.poster_path
    },
  },
  created () {
    this.getMy()
  } 
}
</script>

<style>
.list-box {
  position: relative;
  width : 100%;
  min-height: 100vh;
  justify-content: center;
  align-items:center;
  overflow: hidden;
  padding: 100px;
}
</style>