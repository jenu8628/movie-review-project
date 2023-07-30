<template>
  <div style="margin-top:3%">
    <div class="container d-flex justify-content-between">
      <div>
        <button class="btn btn-secondary ghost-button" @click="sortByTime(pageNationNum)">최신글</button>
        <button class="btn btn-secondary ghost-button" @click="sortByLike(pageNationNum)">인기글</button>
      </div> 
      <div>
        <router-link class="btn btn-secondary ghost-button" to="/community/movie_review_form">리뷰 쓰기</router-link>
        <div class="dropdown">
          <button class="btn btn-secondary ghost-button dropdown-toggle" data-toggle="dropdown">
            {{pageNationNum}}줄 보기
          </button>
          <div class="dropdown-content">
            <option style="border-radius: 10px;" class="btn btn-secondary ghost-button" @click="pageNationNumber(5)">5줄 보기</option>
            <option style="border-radius: 10px;" class="btn btn-secondary ghost-button" @click="pageNationNumber(10)">10줄 보기</option>
            <option style="border-radius: 10px;" class="btn btn-secondary ghost-button" @click="pageNationNumber(15)">15줄 보기</option>
          </div>
        </div> 
      </div>       
    </div>
      <!-- <div class="container text-left ">
        <div class="d-flex row mt-2 mb-4">
          <div class="col-4 movie-title">영화제목</div>
          <div class="col-4 movie-title">글제목</div> 
          <div class="col-2 review-username">작성자</div>
          <div class="col-1 movie-rank">평점</div> 
          <div class="col-2">작성일</div>
        </div>
        <div v-for="(review,idx) in reviewList" :key="idx">
          <div class="row btn-secondary ghost-button d-flex mb-2" @click="onClick(review)">
            <div class="col-4 movie-title">{{review.movie_title}}</div>
            <div class="col-4 movie-title">{{review.title}}</div> 
            <div class="col-2 review-username">{{review.username}} </div>
            <div class="col-1 movie-rank">{{review.rank}}</div> 
            <div class="col-2">{{ getCreatedAt(review) }}</div>
          </div>
        </div>
      </div> -->
      <div class="col-12 mt-5" style="min-height:30vh" v-for="(review,idx) in reviewList" :key="idx">
        <MovieReviewThumbnail :poster="getPoster(review.movie_title)" :review="review"/>
      </div>
    <div class="container my-3">
      <div class="d-flex justify-content-center">
        <nav class="nav">
          <ul class="pagination pagination-sm">
            <li v-for="(cnt,idx) in count" :key="idx">
              <button class="btn btn-secondary ghost-button" @click="viewList(cnt)"> {{cnt}} </button>
            </li>
          </ul>
        </nav>
      </div>
    </div>

  </div>
</template>

<script>
import axios from 'axios'
import moment from 'moment'
import MovieReviewThumbnail from './MovieReviewThumbnail.vue'
import movies from '../../movies.json'

const SERVER_URL = process.env.VUE_APP_SERVER_URL

export default {
  data : function () {
    return {
      MovieReviews : [],
      count : [],
      movieReviewsPage : [],
      reviewList : [],
      likes : 0,
      pageNationNum: 5,
      movies : movies,
    } 
  },
  components : {
    MovieReviewThumbnail
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
    getPoster (movieTitle) {
      const movie = this.movies.find((movie)=>{
        return movie.title === movieTitle
      })
      console.log(movie.poster_path)
      return movie.poster_path
    },

    onClick : function (review) {
      window.location.href=`http://localhost:8080/community/movie_review_detail?review_id=${review.id}`
      // this.$router.push({name : 'movie_review_detail', query : {review_id:review.id}})
    },
    getLikeCount : function (review_id) {
      const config = this.setToken()
      axios.get(`${SERVER_URL}/community/like_movie_review/${review_id}/`,config)
      .then((res)=>{
        this.likes = res.data.like_users
      })
    },
    getCreatedAt : function (review) {
      return moment(review.created_at).startOf('minute').fromNow()   
    },
    sortByLike : function (pageNationNum) {
    const config = this.setToken()
    axios.get(`${SERVER_URL}/community/movie_review_list_order_by_like/`,config)
    .then((res)=>{  
      this.MovieReviews = res.data
      this.page(this.MovieReviews, pageNationNum)
      })
    },
    sortByTime : function (pageNationNum) {
      const config = this.setToken()
    axios.get(`${SERVER_URL}/community/movie_review_list_create/`,config)
    .then((res)=>{  
      this.MovieReviews = res.data
      this.page(this.MovieReviews, pageNationNum)
      })
    },
    viewList(cnt) {
      this.reviewList = this.movieReviewsPage[cnt-1]
      window.scrollTo({top: 0, behavior: 'smooth'});
    },
    page (MovieReviews, pageNationNum) {
      this.count = []
      this.movieReviewsPage = []
      const cnt = parseInt(MovieReviews.length / pageNationNum) + 1
      for (let i = 1; i<=cnt; i++){
        this.count.push(i)
        }
      const count = MovieReviews.length
      var tmp = []
      for (let j = 0; j<count; j++){
        tmp.push(MovieReviews[j])
        if (j % pageNationNum === pageNationNum-1 && j !== 0){
          this.movieReviewsPage.push(tmp)
          tmp = []
        }else if(j === count-1){
          this.movieReviewsPage.push(tmp)
        }
      }this.reviewList = this.movieReviewsPage[0]
    },
    pageNationNumber(event){
      this.pageNationNum = event
      this.page(this.MovieReviews, this.pageNationNum)
    }
  },
  created: function () {
    const config = this.setToken()
    axios.get(`${SERVER_URL}/community/movie_review_list_create/`,config)
    .then((res)=>{  
      this.MovieReviews = res.data
      this.page(this.MovieReviews, 5)
      })
    .catch((err)=>{
      console.log(err)
    })
  }
}
</script>

<style>
.movie-title {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 25%;
  min-width: 25%;
}
/* .movie-rank {
  margin-left : 5%;
  min-width: 10%;
} */
.movie-like {
  min-width: 10%;
}
.review-username {
  min-width: 20%;
}
</style>