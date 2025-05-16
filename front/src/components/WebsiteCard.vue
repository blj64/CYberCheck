<template>
    <div class="rounded-xl shadow p-4 border border-gray-200 bg-white">
      <h2 class="text-lg font-semibold">{{ website.name }}</h2>
      <p class="text-sm text-gray-500 truncate">{{ website.url }}</p>
      <div class="mt-2">
        <span
          class="inline-block rounded-full px-2 py-1 text-xs font-semibold"
          :class="{
            'bg-green-100 text-green-800': website.status === 'up',
            'bg-red-100 text-red-800': website.status === 'down',
            'bg-gray-100 text-gray-800': !website.status
          }"
        >
          {{ website.status || 'unknown' }}
        </span>
      </div>
    </div>
  </template>
  
  <script setup>
  defineProps({
    website: Object
  })
  </script>
  