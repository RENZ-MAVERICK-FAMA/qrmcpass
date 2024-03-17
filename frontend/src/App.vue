<template>
  <div>
    <header>
      <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container">
          <RouterLink class="navbar-brand" to="/">QRMCPASS</RouterLink>
          <button
            class="navbar-toggler"
            type="button"
            data-bs-toggle="collapse"
            data-bs-target="#navbarSupportedContent"
            aria-controls="navbarSupportedContent"
            aria-expanded="false"
            aria-label="Toggle navigation"
          >
            <span class="navbar-toggler-icon"></span>
          </button>
          <div class="collapse navbar-collapse" id="navbarSupportedContent">
            <ul class="navbar-nav me-auto mb-2 mb-lg-0">
              <li class="nav-item">
                <RouterLink class="nav-link" to="/loginUnit" v-if="!authenticated">Unit</RouterLink>
              </li>
              <li class="nav-item">
                <RouterLink class="nav-link" to="/loginTeller" v-if="!authenticated">Teller</RouterLink>
              </li>
              <li class="nav-item">
                <RouterLink class="nav-link" to="/login" v-if="!authenticated">Operator</RouterLink>
              </li>
              <li class="nav-item" v-if="authenticated && show">
                <router-link class="nav-link" to="/home">Home</router-link>
              </li>
              <li class="nav-item" v-if="authenticated">
                <button class="btn btn-link nav-link" @click="logout">Logout</button>
              </li>
            </ul>


            <ul class="navbar-nav ml-auto">
              <li class="nav-item">
                <RouterLink class="nav-link" to="/signup" v-if="!authenticated">Sign Up</RouterLink>
              </li>
              <li class="nav-item">
                <RouterLink class="nav-link" to="/addTeller" v-if="!authenticated">Add Teller</RouterLink>
              </li>
            
            
            </ul>
          </div>
        </div>
      </nav>
    </header>

    <!-- Router view for rendering child components -->
    <RouterView :showHomeButton="showHomeButton" />
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'

const authenticated = ref(localStorage.getItem('access_token') !== null)
const route = useRoute()
const router = useRouter()

// Watch for changes in the authenticated flag
watch(authenticated, (newValue) => {
  if (!newValue) {
    // User is not authenticated
    router.push('/login')
  }
})

// Logout function
const logout = () => {
  localStorage.removeItem('access_token')
  authenticated.value = false
  router.push('/login')
}
</script>

<style scoped>
/* Your scoped styles here */
</style>
