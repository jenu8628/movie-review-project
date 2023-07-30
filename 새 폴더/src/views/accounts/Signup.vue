<template>
<div class="login-box">
  <div class="align-items-center">
  <div>
    회원가입
    <div>
      <input  class="btn btn-secondary login-form my-3" placeholder="아이디" type="text" v-model="credentials.username">
    </div>
    <div>
      <input  class="btn btn-secondary login-form my-3" placeholder="비밀번호" type="password" v-model="credentials.password">
    </div>
    <div>
      <input  class="btn btn-secondary login-form my-3" placeholder="비밀번호 확인" type="password" v-model="credentials.passwordConfirmation">
    </div>
    <div>
      <p>좋아하는 영화 장르를 선택해 주세요.</p>
        <span class="mx-1" v-for="(genre, idx) in genres" :key="idx">
            <input type="checkbox" @click="getFavoriteGenres(idx)" :id="genre.genre">
            <label :for="genre.genre">{{genre.genre}}</label>
        </span>
    </div>
    <button  class="btn btn-secondary login-form my-3" @click="Signup()">회원가입</button>
    </div>
  </div>
</div>
</template>

<script>
import axios from 'axios'
const SERVER_URL = process.env.VUE_APP_SERVER_URL

export default {
  name: 'Signup',
  data : function () {
    return {
      genres : [{'genre':'액션',completed:false},
        {'genre':'모험', completed:false,}, 
        {'genre':'애니메이션', completed:false,},
        {'genre':'코미디', completed:false,},
        {'genre':'범죄', completed:false,},
        {'genre':'드라마', completed:false,},
        {'genre':'가족', completed:false,},
        {'genre':'판타지', completed:false,},
        {'genre':'역사', completed:false,}, 
        {'genre':'공포', completed:false,}, 
        {'genre':'음악', completed:false,}, 
        {'genre':'미스터리', completed:false,},
        {'genre':'로맨스', completed:false,},
        {'genre':'SF', completed:false,}, 
        {'genre':'TV영화', completed:false,},
        {'genre':'스릴러', completed:false,},
        {'genre':'전쟁', completed:false,}, 
        {'genre':'서부', completed:false,}
      ],
      credentials : {
        username : '',
        password : '',
        passwordConfirmation : '',
        favoriteGenres: '',
      }
    }
  },
  methods : {
    Signup : function () {
      for(let i = 0 ; i< this.genres.length ; i++){
        if (this.genres[i].completed){
          this.credentials.favoriteGenres = this.credentials.favoriteGenres + ' ' + this.genres[i].genre
        }
      }
      axios.post(`${SERVER_URL}/accounts/signup/`,this.credentials)
      .then(()=>{
        this.$router.push({name: 'Login'})
      })
      .catch((err)=>{
        console.log(err)
      })
    },
    getFavoriteGenres (idx) {
      this.genres[idx].completed = !this.genres[idx].completed
    }
  }
}
</script>

<style>

</style>