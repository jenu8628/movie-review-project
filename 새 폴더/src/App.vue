<template>
  <div id="app" class="my-1">
    <div class="navbar sticky-top d-flex justify-content-between bg-transparent" v-if="login">
      <div id="nav-left-on-login">
        <router-link class="btn btn-secondary ghost-button" to="/home">Home</router-link> |
        <div class="dropdown">
          <button class="btn btn-secondary ghost-button">게시판</button> |
            <div class="dropdown-content">
              <router-link class="dropdown-nowrap" style="border-radius: 10px; text" to="/community/movie_review_list">영화리뷰게시판</router-link>
              <router-link style="border-radius: 10px;" to="/community/post_list">자유게시판</router-link>
            </div>
          </div>
        <div class="dropdown">
          <button class="btn btn-secondary ghost-button">내 정보</button> 
          <div class="dropdown-content">
            <router-link style="border-radius: 10px; text" to="/community/community_mypage">내 영화리뷰</router-link>
            <router-link style="border-radius: 10px;" to="#" @click.native="logout">로그아웃</router-link><br>
          </div>
        </div>
        <button v-if="is_superuser" class="btn btn-secondary ghost-button" @click="showAdmin">관리자</button>
      </div>
      <div id="nav-right-on-login" class="d-flex">
        <div id="search-container"></div>
        <router-link class="btn btn-secondary ghost-button" @click.native="showSeachrBar" to="#" >검색</router-link>
    </div>
      </div>
    <div class="nav navbar sticky-top d-flex justify-content-between" v-if="!login">
      <div>
      </div>
      <div>
        <router-link class="btn btn-secondary ghost-button" to="/Login" >로그인</router-link> | 
        <router-link class="btn btn-secondary ghost-button" to="/Signup" >회원가입</router-link>
      </div>
    </div>
    <router-view @login="login = true"/>
  </div>
</template>

<script>
import axios from 'axios'
import movies from './movies.json'
const SERVER_URL = process.env.VUE_APP_SERVER_URL

export default {
  data : function () {
    return {
      login : false,
      searchBar : false,
      movies: movies,
      is_superuser : '',
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
    logout : function () {
        localStorage.removeItem('jwt')
        localStorage.removeItem('username')
        localStorage.removeItem('user_id')
        localStorage.removeItem('favorite_genres')
        localStorage.removeItem('is_superuser')
        this.login = false
        this.$router.push({name : 'Login'})
    },
    showSeachrBar : function () {
    if (! this.searchBar) {
      this.searchBar = true
      const serarchContainer = document.querySelector('#search-container')
      serarchContainer.setAttribute("style","position: absolute; z-index: 99;  right: 10%")
      const div = document.createElement('div')
      div.setAttribute("id", "suggestions")

      const inputGroup = document.createElement('div')
      inputGroup.setAttribute('class','input-group')
      inputGroup.setAttribute('style','-webkit-animation: fadein 0.5s;')

      const inputGroupAppend = document.createElement('div')
      inputGroupAppend.setAttribute('class','input-group-append')

      const button = document.createElement('button')
      button.setAttribute('id','searchBtn')
      button.addEventListener('click', this.goDetail )
      button.innerHTML='찾기'

      const input = document.createElement('input')
      input.setAttribute("id", "searchInput")
      input.setAttribute("autocomplete", "off")
      input.setAttribute("class", "btn btn-secondary")
      input.setAttribute("style", "height : 100%")
      input.addEventListener("keyup", this.showSuggestion)

      inputGroupAppend.appendChild(button)
      inputGroup.appendChild(input)
      inputGroup.appendChild(inputGroupAppend)
      serarchContainer.appendChild(inputGroup)
      serarchContainer.appendChild(div)

      }
    else {
      this.searchBar = false
      document.getElementById("suggestions").remove()
      document.getElementById("searchInput").remove()
      document.getElementById("searchBtn").remove()
      }
    },
    goDetail : function () {
      const inputValue = document.querySelector('#searchInput').value
      this.searchBar = false      
      document.getElementById("suggestions").remove()
      document.getElementById("searchInput").remove()
      document.getElementById("searchBtn").remove()
      window.location.href=`http://localhost:8080/movie_detail?movie_title=${inputValue}`
      // this.$router.push({name : 'movie_detail', query : {movie_title :inputValue}})
    },
    showSuggestion : function (event) {
      const searchInput = document.querySelector('#searchInput').value
      const suggestionsPanel = document.querySelector('#suggestions')
      suggestionsPanel.innerHTML = '';
      const suggestions = this.movies.filter(function(movie) {
        return movie.title.toLowerCase().startsWith(searchInput)
      })
      suggestions.forEach(function(suggested) {
        const div = document.createElement('div')
        div.addEventListener("click", function (){
          window.location.href=`http://localhost:8080/movie_detail?movie_title=${suggested.title}`
          // const searchInput = document.querySelector('#searchInput')
          // searchInput.value = suggested.title
          })
        div.setAttribute("class","btn-secondary ghost-button block change-cursor")
        div.innerHTML = suggested.title
        suggestionsPanel.appendChild(div)
      })
      if (searchInput === '') {
        suggestionsPanel.innerHTML = ''
      }
      if (event.key=='Enter'){
        console.log('enter!!!!!!!!')
      }
    },
    showAdmin () {
      const config = this.setToken()

      axios.get(`${SERVER_URL}/accounts/identify_user_superuser/`,config)
      .then((res)=>{
        if(res.data.is_superuser){
          window.location.href = "http://127.0.0.1:8000/admin/"
        }
        else{
          alert('잘못된 접근')
        }
      })
      
      
    }
  },
  created: function () {
    const tmp = localStorage.getItem('username')
    if (tmp === 'admin'){
      this.is_superuser = true
    }
    else {
      this.is_superuser = false
    }
    console.log(this.is_superuser)
    const token = localStorage.getItem('jwt')
    if (token) {
      this.login = true
    }
  }
}
</script>

<style>
#app {
  text-align: center;
  color : white;
  z-index: 1;
  font-weight: bold;
}
#app a{
  color : white
}
#nav {
  padding: 30px;
  position: fixed;
  top:0;
}

#nav a {
  font-weight: bold;
}

/* 투명한버튼*/
/* Dropdown Button */
.ghost-button {
  background-color:transparent;  
  border: none;
}
.change-cursor {
  cursor: pointer;
}
/* The container <div> - needed to position the dropdown content */
.dropdown {
  color : white;
  position: relative;
  display: inline-block;
}

/* Dropdown Content (Hidden by Default) */
.dropdown-content {
  display: none;
  position: absolute;
  /* background-color: #2e2b2b; */
  min-width: 120px;
  /* box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2); */
  font-size : 12px;
  z-index: 1;
  border: solid;
  border-color: rgb(54, 52, 52);
  background-color: black;
  border-radius: 15px / 15px
}


/* 주르륵 나오는 컨텐츠  */
.dropdown-content a {
  padding: 12px 16px;
  text-decoration: none;
  display: block;
}

.dropdown-nowrap {
  white-space: nowrap;
}
/* 호버했을 때 컨텐츠 배경색 */
.dropdown-content a:hover {background-color:#6c757d;}

/*호버했을 때 하위 컨텐츠 블럭으로 보여주기*/ 
.dropdown:hover .dropdown-content {display: block !important;}

@-webkit-keyframes fadein {
    from { opacity: 0; }
    to   { opacity: 1; }
}
@-webkit-keyframes fadeout {
    from { opacity: 0; }
    to   { opacity: 1; }
}
</style> 
