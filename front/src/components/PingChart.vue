<template>
    <Line :data="chartData" :options="chartOptions" />
  </template>
  
  <script setup>
  import { Line } from 'vue-chartjs'
  import {
    Chart as ChartJS,
    Title,
    Tooltip,
    Legend,
    LineElement,
    CategoryScale,
    LinearScale,
    PointElement
  } from 'chart.js'
  
  ChartJS.register(Title, Tooltip, Legend, LineElement, CategoryScale, LinearScale, PointElement)
  
  const props = defineProps({
    results: Array // recent_check_results
  })
  
  const chartData = {
    labels: props.results.map(r => new Date(r.checked_at).toLocaleTimeString()),
    datasets: [
      {
        label: 'Ping (ms)',
        data: props.results.map(r => r.ping),
        borderColor: '#ffffff',
        backgroundColor: 'rgba(255, 255, 255, 0.2)',
        tension: 0.3
      }
    ]
  }
  
  const chartOptions = {
    responsive: true,
    plugins: {
      legend: {
        labels: { color: 'white' }
      }
    },
    scales: {
      x: {
        ticks: { color: 'white' }
      },
      y: {
        ticks: { color: 'white' },
        beginAtZero: true
      }
    }
  }
  </script>
  