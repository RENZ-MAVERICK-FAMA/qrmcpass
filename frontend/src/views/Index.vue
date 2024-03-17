<template>
    <div>
      <h1>Hello, World!</h1>
      <button @click="sendMessage">Send Message</button>
      <div>{{ response }}</div>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  import io from 'socket.io-client';
  
  const socket = io('http://127.0.0.1:9000');
  const response = ref('');
  
  socket.on('response', (data) => {
    response.value = data.data;
  });
  
  const sendMessage = () => {
    socket.emit('message', 'Hello from Vue.js!');
  };
  </script>
  