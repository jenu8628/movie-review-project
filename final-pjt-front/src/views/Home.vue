<template>
  <div style="text-align: center;">
    <h3>추천 영화</h3>
    <div class="container">
      <div class="row d-flex justify-content-around">
        <div v-for="(recommend, i) in recommends" :key="i">
          <div class="cardbox">
            <img @click="goDetail(recommend.title)" :src="recommend.poster_path" style="width:300px" alt="...">
          </div>
        </div>
      </div>
    </div>
    <h3>인기 영화</h3>
    <div class="container">
      <div class="row justify-content-around">
          <div v-for="(item, $index) in list" :key="$index">
            <div class="cardbox">
              <img @click="goDetail(item.title)" :src="item.poster_path" style="width:300px" alt="...">
            </div>
          </div>
        <infinite-loading class="col-6 loader" spinner="bubbles" @infinite="infiniteHandler"></infinite-loading>
      </div>
    </div>
  </div>
</template>

<script>
import _ from 'lodash'
import movies from '../movies.json'

export default {
  name: 'Home',
  data () {
    return {
      page : 1,
      list : [],
      movies: movies,
      recommends : [],
      genre:  JSON.parse(localStorage.getItem('favorite_genres')),
    }
  },
  methods: {
    infiniteHandler($state) {
      if (this.page > 1){
        setTimeout(()=>{
          if (this.page < this.movies.length - 6) {
            this.page += 6;
            for (let i=this.page;i<this.page+6;i++){
              this.list.push(this.movies[i]);
            }
            $state.loaded();
          } else {
            $state.complete();
          }
        },1500)
      }
      else {
        if (this.page < this.movies.length - 6) {
          this.page += 6;
          for (let i=this.page;i<this.page+6;i++){
            this.list.push(this.movies[i]);
          }
          $state.loaded();
        } else {
          $state.complete();
        }
      }
    },
    getRecommend() {
      const genre = this.genre
      
      if (Array.isArray(genre) && genre.length) {
        const recommends = this.movies.filter(function(movie) {
        const tmp = movie.genre_ids.filter(gen => genre.includes(gen))
        return tmp.length
      })

        if (recommends.length > 6){
          this.recommends = _.sampleSize(recommends, 6)
        }
        else {
          this.recommends = recommends
          const tmp = _.sampleSize(this.movies, 6-this.recommends.length)
          this.recommends.push(...tmp)
        }
      }
      else {
        this.recommends = _.sampleSize(this.movies, 6)
      }

    },
    goDetail (movieTitle) {
      window.location.href=`http://localhost:8080/movie_detail?movie_title=${movieTitle}`
    },
    // async fetchData() {
    //   console.log(this.getFavoriteGenre())
    //     return await this.getFavoriteGenre().then()
    //   }
  },
  created () {
    setTimeout(()=>{},1000)
    this.genre = JSON.parse(localStorage.getItem('favorite_genres'))
    this.getRecommend()
    this.infiniteHandler()
  }
}
</script>

<style>

.cardbox {
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 10px;
  transition: 0.5s;
}
.cardbox {
  max-width: 100%;
  opacity: 0.4;
  transition: 0.5s;
}
.cardbox:hover{
  opacity: 1;
}
.cardbox:before {
  content : '';
  position: absolute;
  top: -2px;
  left: -2px;
  right: -2px;
  bottom: -2px;
  background: #fff;
  z-index: -1;
} 
.cardbox:after {
  content : '';
  position: absolute;
  top: -2px;
  left: -2px;
  right: -2px;
  bottom: -2px;
  background: #fff;
  z-index: -2;
  filter : blur(40px);
}
.loader{
  transform: scale(2);
}
</style>
