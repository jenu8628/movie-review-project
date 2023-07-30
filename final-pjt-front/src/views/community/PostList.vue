<template>
  <div style="margin-top:10%">
    <div class="container d-flex justify-content-between">
      <div>
        <button class="btn btn-secondary ghost-button" @click="sortByTime">최신글</button>
        <button class="btn btn-secondary ghost-button" @click="sortByLike">인기글</button>
      </div> 
      <div>
        <router-link class="btn btn-secondary ghost-button" to="/community/post_form">글쓰기</router-link>
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
    <div class="container text-left">
      <div class="d-flex row row mt-2 mb-4">
        <div class="col-4 post-title">제목</div>
        <div class="col-4 post-content">내용</div> 
        <div class="col-2 post-username">작성자</div>
        <div class="col-2" >작성일</div>       
      </div>

      <div v-for="(review,idx) in postList" :key="idx">
        <div class="row btn-secondary ghost-button d-flex mb-2" @click="onClick(review)">
          <div class="col-4 post-title">{{review.title}}</div>
          <div class="col-4 post-content">{{review.content}}</div> 
          <div class="col-2 post-username">{{review.username}} </div>
          <div class="col-2">{{ getCreatedAt(review) }}</div>
        </div>
      </div>
    </div>
    <div class="container my-3">
      <div class="d-flex justify-content-center">
        <nav class="nav">
          <ul class="pagination pagination-sm">
            <li v-for="(cnt,idx) in count" :key="idx">
              <button class="btn btn-secondary ghost-button" :id="cnt" @click="viewList(cnt)"> {{cnt}} </button>
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

const SERVER_URL = process.env.VUE_APP_SERVER_URL

export default {
  data : function () {
    return {
      Posts : [],
      count : [],
      postReviewsPage : [],
      postList : [],
      pageNationNum : 10,
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
    onClick : function (review) {
      window.location.href=`http://localhost:8080/community/post_detail?review_id=${review.id}`

      // this.$router.push({name : 'post_detail', params : {review_id:review.id}})
    },
    getCreatedAt : function (review) {
      return moment(review.created_at).startOf('minute').fromNow()   
    },
    sortByLike : function () {
      const config = this.setToken()
      axios.get(`${SERVER_URL}/community/post_list_order_by_like/`,config)
      .then((res)=>{  
        this.Posts = res.data
        this.post(this.Posts, this.pageNationNum)
      })
    },
    sortByTime : function () {
      const config = this.setToken()
      axios.get(`${SERVER_URL}/community/post_list_create/`,config)
      .then((res)=>{  
        this.Posts = res.data
        this.post(this.Posts, this.pageNationNum)
      })
    },
    viewList (cnt) {
      this.postList = this.postReviewsPage[cnt-1]
    },
    post(Posts, pageNationNum) {
      this.postReviewsPage = []
      this.count = []
      const cnt = parseInt(Posts.length / pageNationNum) + 1
      for (let i = 1; i<=cnt; i++){
        this.count.push(i)
        }
      const count = Posts.length
      var tmp = []
      for (let j = 0; j<count; j++){
        tmp.push(Posts[j])
        if (j % pageNationNum === pageNationNum - 1 && j !== 0){
          this.postReviewsPage.push(tmp)
          tmp = []
        }else if(j === count-1){
          this.postReviewsPage.push(tmp)
        }
      }this.postList = this.postReviewsPage[0]
    },
    pageNationNumber (event) {
      this.pageNationNum = event
      this.post(this.Posts, this.pageNationNum)
    }
  },
  created: function () {
    const config = this.setToken()
    axios.get(`${SERVER_URL}/community/post_list_create/`,config)
    .then((res)=>{  
      this.Posts = res.data
      this.post(this.Posts, this.pageNationNum)
      })
    .catch((err)=>{
      console.log(err)
    })
  }
}
</script>

<style>
.post-title {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 30%;
  min-width: 20%;
}
.post-content {
  margin-left : 5%;
  min-width: 20%;
  max-width: 20%;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.post-like {
  min-width: 8%;

}
.post-username {
  margin-left : 5%;
  min-width: 15%;
}
</style>