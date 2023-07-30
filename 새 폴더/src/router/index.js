import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import Main from '../views/Main.vue'
import MovieDetail from '../views/MovieDetail.vue'
import Mypage from '../views/community/Mypage.vue'
import CreateMovieReview from '../views/community/CreateMovieReview.vue'
import MovieReviewDetail from '../views/community/MovieReviewDetail.vue'
import MovieReviewForm from '../views/community/MovieReviewForm.vue'
import MovieReviewUpdate from '../views/community/MovieReviewUpdate.vue'
import MovieReviewList from '../views/community/MovieReviewList.vue'
import PostList from '../views/community/PostList.vue'
import PostDetail from '../views/community/PostDetail.vue'
import PostForm from '../views/community/PostForm.vue'
import PostUpdate from '../views/community/PostUpdate.vue'
import CreatePost from '../views/community/CreatePost.vue'
import Login from '../views/accounts/Login.vue'
import Signup from '../views/accounts/Signup.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Main',
    component: Main
  },
  {
    path: '/home',
    name: 'Home',
    component: Home
  },
  {
    path: '/movie_detail',
    name: 'movie_detail',
    component: MovieDetail
  },
  {
    path: '/community/create/movie_review',
    name: 'community_create_movie_review',
    component: CreateMovieReview
  },
  {
    path: '/community/community_mypage',
    name: 'Mypage',
    component: Mypage
  },
  {
    path: '/community/movie_review_detail/',
    name: 'movie_review_detail',
    component: MovieReviewDetail,
  },
  {
    path: '/community/post_detail/',
    name: 'post_detail',
    component: PostDetail,
  },
  {
    path: '/community/movie_review_form',
    name: 'movie_review_form',
    component: MovieReviewForm,
  },
  {
    path: '/community/movie_review_update',
    name: 'movie_review_update',
    component: MovieReviewUpdate,
  },
  {
    path: '/community/movie_review_list',
    name: 'movie_review_list',
    component: MovieReviewList,
  },
  {
    path: '/community/post_list',
    name: 'post_list',
    component: PostList,
  },
  {
    path: '/community/post_update',
    name: 'post_update',
    component: PostUpdate,
  },
  {
    path: '/community/post_form',
    name: 'post_form',
    component: PostForm,
  },
  {
    path: '/community/create/post',
    name: 'community_create_post',
    component: CreatePost
  },
  {
    path: '/Signup',
    name: 'Signup',
    component: Signup
  },
  {
    path: '/Login',
    name: 'Login',
    component: Login
  },

]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
