<template>

    <div>
      <h2 align="center">Top Up Balance</h2>
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
      <div class="container">
        <div class="row justify-content-center">
          <div class="col-md-6">
            <form @submit.prevent="topup">
              <div class="form-group">
                <label for="unit">Select Unit:</label>
                <select v-model="selectedUnit" class="form-control" id="unit" name="unit" required>
                  <option v-for="unit in units" :key="unit.id" :value="unit.id">{{ unit.unit_info }}</option>
                </select>
              </div>
              <label for="branch">Branch:</label>
              <select v-model="selectedBranch" name="branch" id="branch" required>
                <option value="market">Market</option>
              </select><br> 
              <div class="form-group">
                <label for="amt">Amount to Top Up:</label>
                <input v-model="amount" type="number" class="form-control" id="amt" name="amt" placeholder="Enter amount" required>
              </div>
              <button type="submit" class="btn btn-primary">Top Up</button>
            </form>
          </div>
        </div>
      </div>
    </div>

  </template>
  
  <script>
import { ref, toHandlers, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import axios from 'axios'
import io from 'socket.io-client';
const authenticated = ref(false)
const route = useRoute()
const router = useRouter()
const socket = io('http://127.0.0.1:9000');

export default {
    data() {
        return {
            units: [],
            selectedBranch:'',
 
            selectedUnit:'',
            amount:'',
      success: '',
      error: ''
        };
    },
    created() {
        this.fetchUnits();
        
   
    },
    setup() {
    const teller = ref({ id: null, username: '', first_name: '', last_name: '' })

    axios.get('http://127.0.0.1:9000/Teller', {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('access_token')}`
      }
    })
    .then(response => {
      teller.value = response.data
    })
    .catch(error => {
      console.error('Error fetching user:', error)
    })

    return { teller }
  },
    methods: {
      clearError() {
    this.error = '';
  },
  
  clearSuccess() {
    this.success = '';
  } ,
        fetchUnits() {
    axios.get('http://127.0.0.1:9000/units', {
        headers: {
            Authorization: `Bearer ${localStorage.getItem('access_token')}`
        }
    })
    .then(response => {
        console.log(response.data.units); // Check if units are received
        this.units = response.data.units;
        this.fetchBalances();
    })
    .catch(error => {
        console.error('Error fetching user units:', error);
    });
},
fetchBalances() {
    // Fetch balances for each unit
    this.units.forEach(unit => {
        axios.get(`http://127.0.0.1:9000/unit/${unit.id}/balances`, {
            headers: {
                Authorization: `Bearer ${localStorage.getItem('access_token')}`,
    'Content-Type': 'application/json'
            }
        })
        .then(response => {
            console.log(response.data.balances); // Check if balances are received
            unit.balances = response.data.balances; // Directly assign balances to unit
        })
        .catch(error => {
            console.error('Error fetching balances for unit:', unit.id, error);
        });
    });
},topup() {
  let data = {
    selectedBranch: this.selectedBranch,
    selectedUnit: this.selectedUnit,
    amount: this.amount,
    teller: this.teller.id,
  };

  axios.post('http://127.0.0.1:9000/topup', data, {
    headers: {
      Authorization: `Bearer ${localStorage.getItem('access_token')}`,
      'Content-Type': 'application/json'
    }
  })
  .then(response => {
    console.log('Top up response:', response.data);
    if (response.data.message === 'Top up successful!') {
      this.selectedBranch = '';
      this.selectedUnit = '';
      this.amount = '';
      teller: this.teller.id,
      this.success = 'Topup successful!';
    } else {
      console.error('Top up failed:', response.data.message);
      alert('Top up failed. Please try again.');
    }
  })
  .catch(error => {
    console.error('An error occurred:', error);
   
    this.error = 'An error occurred. Please try again.';
  });
}
  }};
</script>
  
  <style>
  /* Add your CSS styles here */
  </style>