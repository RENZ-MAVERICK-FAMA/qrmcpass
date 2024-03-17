<template>
  <div>
    <p v-if="authenticated">Authenticated</p>
    <p v-else>Not Authenticated</p>
    <div v-if="error" class="alert alert-danger" role="alert">
  {{ error }}
  <button @click="clearError" class="close" data-dismiss="alert">
    <span aria-hidden="true">&times;</span>
  </button>
</div>  
      <div v-if="success" class="alert alert-success" role="alert">
  {{ success }}
  <button @click="clearSuccess" class="close" data-dismiss="alert">
    <span aria-hidden="true">&times;</span>
  </button>
</div>
<div v-if="loginError" class="alert alert-danger" role="alert">
          {{ loginError }}
        </div>
    <div>
      
      <h1>Add Unit</h1>
      <form @submit.prevent="addunit">
        <label for="unittype">Unit Type:</label>
        <select v-model="unittype" id="unittype">
          <option value="motorela">Motorela</option>
          <option value="multicab">Multicab</option>
          <option value="bus">Bus</option>
        </select><br><br>
        <label for="color">Color:</label><br>
        <input v-model="color" type="text" id="color" required><br><br>
        <label for="unitinfo">Unit Information:</label><br>
        <input v-model="unitinfo" type="text" id="unitinfo" required >
        
        <br>
        <div class="form-group">
          <label for="password1">Password</label>
          <input
            type="password"
            class="form-control"
            id="password1"
            v-model="password1"
            placeholder="Enter password"
            required />
        </div>
        <div class="form-group">
          <label for="password2">Password (Confirm)</label>
          <input
            type="password"
            class="form-control"
            id="password2"
            v-model="password2"
            placeholder="Confirm password"
            required />
        </div><br>
        <button type="submit">Add Unit</button>
      </form>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
export default {
  data() {
    return {
      unittype:'',
      color:'',
      unitinfo:'',
      password1: '',
      password2: '',
      authenticated:true,
      success:'',
      error:'',
      
    };
  },
  methods: {
    clearError() {
    this.error = '';
  },
  
  clearSuccess() {
    this.success = '';
  } ,
  addunit() {
    let formData = new FormData();
    formData.append('color', this.color);
    formData.append('unitinfo', this.unitinfo);
    formData.append('unittype', this.unittype);
    formData.append('password1', this.password1);
    formData.append('password2', this.password2);
    axios.post('http://127.0.0.1:9000/addunit', formData, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('access_token')}`
      }
    })
    .then(response => {
      this.color = '';
      this.unitinfo = '';
      this.unittype = '';
      this.password1 = '';
      this.password2 = '';
      this.success = 'Unit Added Successfully!';
    })
    .catch(error => {
      console.error(error);
      this.error = 'Unit Addition Failed';
    });
  }
}
};
</script>

<style>
/* Add your CSS styles here */
</style>