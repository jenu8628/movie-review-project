<template>
  <div v-if="detailPageStatus">
    <div v-if="script" class="d-flex flex-column box" id="script">
      <div style="font-size:2.5rem;" >{{script}}</div>
      <div style="font-size:1.5rem;color:#ededed;" >{{scriptActor}}</div>
    </div>
    <div v-else>
      <div style="font-size:2.5rem;" id="script"></div>
    </div>
    <div v-if="selectedVideo" class="box">
      <iframe :src="selectedVideoURI" frameborder="0" allowfullscreen></iframe>
    </div>
    <div v-else>
      <img :src="targetInfo.poster_path" class="detail-img" id="posterImg" width="300px" alt="">
    </div>
    <div class="box" id="bottom">
      <div class="bottom-h2">{{targetInfo.title}} {{targetInfo.original_title}}</div>
      <div class="bottom-p"><P>{{targetInfo.overview}}</P></div>
    </div>
    <div class="box d-flex" id="actorInfo">
      <div v-for="(info,idx) in actorInfo.info" :key="idx">
        <div class="flex-column"><img :src="info.img" alt=""><p>{{info.name}}</p></div>
      </div>
    </div>
    <h3 v-if="!targetInfo.overview">overview does not exist</h3>
  </div>
  <div v-else>
    {{pageAlert()}}
  </div>
</template>

<script>
import movies from '../movies.json'
import axios from 'axios'

// const API_KEY = 'AIzaSyA5zZ36EzCTYPdBsC5E3mMlqzYEVZUgEwc' // 병훈
const API_KEY = 'AIzaSyACKDTuGiC526w2yHQO-yCfXhrUAjReEdo' // 현우
const API_URL = 'https://www.googleapis.com/youtube/v3/search'
const SERVER_URL = process.env.VUE_APP_SERVER_URL

export default {
  data : function () {
    return {
      targetMovieTitle : this.$route.query.movie_title,
      targetInfo : [],
      movies: movies,
      selectedVideo : [],
      selectedVideoURI : '',
      detailPageStatus : false,
      actorInfo : [],
      script : '',
      scriptActor : '',
    }
  },
  created : function () {
    this.getVideo(this.targetMovieTitle)
    if (this.getVideo){
      window.addEventListener('scroll',this.onScrollIframe)
    }
    else {
      window.addEventListener('scroll',this.onScrollImg)
    }
    for (let i=0;i<this.movies.length;i++){
      if(this.movies[i].title===this.targetMovieTitle){
        this.targetInfo = movies[i]
        this.detailPageStatus = true
        break
      }
    }
    if (this.detailPageStatus) {
      axios.get(`${SERVER_URL}/community/get_movie_info/${this.$route.query.movie_title}`,{
        params : {
          movie_title : this.targetInfo.title,
          pubdate : this.targetInfo.release_date,
        }
      })
      .then((res)=>{
        this.actorInfo = res.data
        this.script = res.data.script
        this.scriptActor = res.data.script_actor
      })
    }

  },
  destroyed () {
    if (this.getVideo) {
    window.removeEventListener('scroll',this.onScrollIframe)
    }
    else {
    window.removeEventListener('scroll',this.onScrollImg)
    }
  },
  methods : {
    pageAlert : function () {
      alert('검색어를 다시 입력해주세요')
    },
    onScrollIframe : function () {
      const vh = window.innerHeight

      const iframe = document.querySelector('iframe')
      const bottom = document.querySelector('#bottom')
      const script = document.querySelector('#script')
      const actorInfo = document.querySelector('#actorInfo')
      
      let scriptVal = 1 + window.scrollY/-vh
      let value = window.scrollY/vh  
      let bottomVal = -1.2 + window.scrollY/vh 
      let actorInfoVal = -2.2 + window.scrollY/vh 

      iframe.style.opacity = value
      bottom.style.opacity = bottomVal
      script.style.opacity = scriptVal
      actorInfo.style.opacity = actorInfoVal
    },
    onScrollImg : function () {
      const vh = window.innerHeight

      const image = document.querySelector('posterImg')
      const bottom = document.querySelector('#bottom')
      const script = document.querySelector('#script')
      const actorInfo = document.querySelector('#actorInfo')
      
      let scriptVal = 1 + window.scrollY/-vh 
      let value = window.scrollY/vh  
      let bottomVal = -1.2 + window.scrollY/vh 
      let actorInfoVal = -2.2 + window.scrollY/vh 

      image.style.opacity = value
      bottom.style.opacity = bottomVal
      script.style.opacity = scriptVal
      actorInfo.style.opacity = actorInfoVal
    },
    getVideo : function (targetMovieTitle) {
      const params = {
        key: API_KEY,
        part: 'snippet',
        type: 'video',
        maxResults : 10,
        q: targetMovieTitle,
      }
      axios.get(API_URL, {params,})
      .then((res) => {
        const videos = res.data.items.filter((item)=>{
          return (item.snippet.title.includes("예고") || item.snippet.title.includes("영화") || item.snippet.title.includes("4K")|| item.snippet.title.includes("리뷰") )
        })
        if (!videos ) {
          this.selectedVideo = ''
          this.selectedVideoURI = ''
        }
        else {
          this.selectedVideo = videos[0]
          this.selectedVideoURI = this.getVideoURI(this.selectedVideo)
        }
      })
      .catch((err) => {
        console.log(err)
      })
    },
    getVideoURI : function (video) {
      const videoId = video.id.videoId
      return `https://www.youtube.com/embed/${videoId}?controls=0&rel=0&autoplay=1&mute=1&loop=1`
    }
  },
}
</script>

<style>
iframe {
  position: absolute;
  top: 0;
  Left : 0;
  width : 100%;
  height : 100%;
  object-fit: cover;
  pointer-events: none;
}
.detail-img {
  pointer-events: none;
}

</style>