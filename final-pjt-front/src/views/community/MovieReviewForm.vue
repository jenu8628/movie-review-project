<template>
  <div class="container text-center" style="width:50% ;margin-top : 10%">
    <div class="text-left my-3">Title</div>
    <div><input class="text-left btn btn-secondary" type="text" style="width:100%" v-model="MovieReview.title"></div>
    <div class="text-left my-3">Movie Title</div>
    <div id="movie-title-container">
      <input class="text-left btn btn-secondary" type="text" style="width:100%" id="movieTitleInput"  autocomplete="off" @keyup="showSuggestion">
    </div>
    <div class="text-left my-3">Content</div>
    <div><input class="text-left btn btn-secondary" type="text" style="width:100% ; height:100px;" v-model="MovieReview.content"></div>
    <div class="text-left my-3">Rank</div>
    <div style=" color:#545454;font-size : 1.5rem" id="star-rank">
      <span class="change-cursor mx-1" @click="starClick(1)" @mouseover="fillStar(1)" @mouseout="clearStar" id="star-1">★</span>
      <span class="change-cursor mx-1" @click="starClick(2)" @mouseover="fillStar(2)" @mouseout="clearStar" id="star-2">★</span>
      <span class="change-cursor mx-1" @click="starClick(3)" @mouseover="fillStar(3)" @mouseout="clearStar" id="star-3">★</span>
      <span class="change-cursor mx-1" @click="starClick(4)" @mouseover="fillStar(4)" @mouseout="clearStar" id="star-4">★</span>
      <span class="change-cursor mx-1" @click="starClick(5)" @mouseover="fillStar(5)" @mouseout="clearStar" id="star-5">★</span>
    </div>
    <button class="btn btn-secondary my-3" @click="createReview">submit your review</button>
  </div>
</template>
<script>
import axios from 'axios'
import movies from '@/movies.json'

const SERVER_URL = process.env.VUE_APP_SERVER_URL

export default {
  data : function () {
    return {
      MovieReview : {
        rank : 0,
        content : '',
        movie_title : '',
        title : '',
        username : localStorage.getItem('username'),
      },
      starStatus : false,
      movies : movies,
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
    fillStar : function (count) {
      if (this.starStatus){
        return
      }
      for (let i=1;i<count+1;i++){
        const star = document.querySelector(`#star-${i}`)
        star.classList.add("fill-star")
      }
    },
    clearStar : function () {
      if (this.starStatus){
        return
      }
      for (let i=1;i<6;i++){
        const star = document.querySelector(`#star-${i}`)
        star.setAttribute("class","change-cursor mx-1")
      }
    },
    starClick : function (count) {
      this.starStatus = !this.starStatus
      if (this.starStatus) {
        this.MovieReview.rank = count 
      }
      else {
        this.MovieReview.rank = 0
      }
    },
    createReview : function () {
      if (this.MovieReview.rank === 0) {
        alert('chose rank')
        return
      }
      const movieTitleInput = document.querySelector('#movieTitleInput').value
      const isContained = this.movies.filter(function(movie) {
        return movie.title=== movieTitleInput
      })
      if (isContained.length===0){
        alert('chose right movie title')
        return
      }
      else {
        this.MovieReview.movie_title = movieTitleInput
      }
      const config = this.setToken()
      const movieReview = this.MovieReview
      axios.post(`${SERVER_URL}/community/movie_review_list_create/`,movieReview, config)
      .then(()=>{
        this.$router.push({name : "movie_review_list"})
      })
      .catch((err)=>{
        console.log(err)
      })
    },
    showSuggestion : function (event) {
      const suggestionsContainer = document.querySelector('#movie-title-container')
      if (!document.getElementById("movie-title-suggestions")){
        const tmp = document.createElement('div')
        tmp.setAttribute('id','movie-title-suggestions')
        suggestionsContainer.appendChild(tmp)
      }
      const suggestionsPanel = document.querySelector('#movie-title-suggestions')
      suggestionsPanel.innerHTML = '';
      suggestionsContainer.appendChild(suggestionsPanel)
      const movieTitleInput = document.querySelector('#movieTitleInput').value
      const suggestions = this.movies.filter(function(movie) {
        return movie.title.toLowerCase().startsWith(movieTitleInput)
      })
      suggestions.forEach(function(suggested) {
        const div = document.createElement('div')
        div.setAttribute("class","btn-secondary ghost-button block")
        div.innerHTML = suggested.title
        div.addEventListener("click", function (){
          const movieTitleInput = document.querySelector('#movieTitleInput')
          movieTitleInput.value =  suggested.title
          document.getElementById("movie-title-suggestions").remove()
        })
        div.setAttribute("class","btn-secondary ghost-button block change-cursor")
        suggestionsPanel.appendChild(div)
      })
      if (movieTitleInput === '') {
        suggestionsPanel.innerHTML = ''
      }
      if (event.key=='Enter'){
        console.log('enter!!!!!!!!')
      }
    }
  }
}
</script>

<style>
.fill-star{
  color : #fff;
}
</style>