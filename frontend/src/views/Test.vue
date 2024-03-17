<template>
  <div>
    <h1>Transactions</h1>
    <table class="table">
      <thead>
        <tr>
          <th>Amount</th>
          <th>Date</th>
          <th>Branch</th>
          <th>Date of Payment</th>
          <th>Type</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="transaction in transactions" :key="transaction.id">
          <td>{{ transaction.amount }}</td>
          <td>{{ transaction.date }}</td>
          <td>{{ transaction.branch }}</td>
          <td>{{ transaction.date_of_payment }}</td>
          <td>{{ transaction.type }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      transactions: []
    };
  },
  created() {
    this.fetchTransactions();
  },
  methods: {
    fetchTransactions() {
      const transactions = ref({ id: null, amount: '', 	date_of_payment: '', date: '',branch:'',type:'' })

      axios.get('http://127.0.0.1:9000/transactions', {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('access_token')}`
        }
      })
      .then(response => {
        this.transactions = response.data.transactions;
      })
      .catch(error => {
        console.error('Error fetching transactions:', error);
      });
    }
  }
};
</script>
