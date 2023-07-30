<template>
  <div>
    <div class="box">

      <div>
        <h1 class="box-above" id="h1-above" style="font-size: 3.5rem; opacity:1; z-index:1;">
          영화 리뷰, 커뮤니티, 지금 바로 함께하세요.
        </h1>
        <h2 class="box-above" id="h2-above" style="font-size: 1.5rem; opacity:0.6; z-index:1;">
          매주 5백 여편의 영화 리뷰가 업데이트 되는, 국내 최대 영화 커뮤니티 
        </h2>
        <img class="top-background" style="opacity : 0.8" src="https://an2-img.amz.wtchn.net/image/v1/watcha/image/upload/v1603708966/cmiozflbxxrh1jiekdrv.webp" alt="">
      </div>
    </div>
    <div class="box" id="bottom">
      <div class="bottom-h2">

      </div>
      <!-- <div class="bottom-h2 mx-5 " style="text-align: left; writing-mode: vertical-rl; text-orientation: upright;">
        <span class="pt-10">불태웠습니다..</span><br> 
        <span>하얗게</span><br> 
      </div>
      <div class="bottom-p">
        <img src="https://img1.daumcdn.net/thumb/R720x0.q80/?scode=mtistory2&fname=http%3A%2F%2Fcfs2.tistory.com%2Fupload_control%2Fdownload.blog%3Ffhandle%3DYmxvZzE4OTQzQGZzMi50aXN0b3J5LmNvbTovYXR0YWNoLzAvMjEuanBn" alt=""></div> -->
      <div class="bottom-p">“지금까지 이런 영화 리뷰 사이트는 없었다. 이것은 영화 리뷰사이트인가, 커뮤니티 사이트인가. 싸피영화통입니다”</div>
    </div>
  </div>
</template>

<script>

export default {

  created () {
    window.addEventListener('scroll',this.onScroll)
  },
  destroyed () {
    window.removeEventListener('scroll',this.onScroll)
  },
  methods : {
    onScroll : function () {
      const vh = window.innerHeight

      const img = document.querySelector('img')
      const h1 = document.querySelector('#h1-above')
      const h2 = document.querySelector('#h2-above')
      const bottom = document.querySelector('#bottom')
      
      let topImgVal = 0.8 + window.scrollY/-vh
      let topTextVal1 = 1 + window.scrollY/-vh
      let topTextVal2 = 0.6 + window.scrollY/-vh
      let bottomVal = window.scrollY/vh - 0.3

      img.style.opacity = topImgVal
      h1.style.opacity = topTextVal1
      h2.style.opacity = topTextVal2
      bottom.style.opacity = bottomVal
    },
  },
}

</script>

<style>
body {
  background : #000;
}
.box {
  position: relative;
  width : 100%;
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items:center;
  overflow: hidden;
  padding: 100px;
}
.box-above{
  position: relative;
  width : 100%;
  display: flex;
  justify-content: center;
  align-items:center;
}
.top-background {
  position: absolute;
  top: 0;
  Left : 0;
  width : 100%;
  height : 100%;
  object-fit: cover;
  pointer-events: none;
}
.bottom-h2 {
  position: relative;
  color : #fff;
  font-size: 3em;
}

.bottom-p {
  position: relative;
  color : #fff;
  font-size: 1.2em;
}
</style>