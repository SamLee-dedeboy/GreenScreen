<script setup lang="ts">
import { Ref, VueElement, ref } from 'vue'
import * as vue from 'vue'

const emit = defineEmits(['search_completed'])
const search_keyword = ref('')
const search_loading = ref(false)


const server_address = 'http://127.0.0.1:5000/'
async function handleSearch(channel_url: string) {
    search_loading.value = true
    await fetch(`${server_address}/channel`,
    {
      method: "POST",
      headers: {
          "Accept": "application/json",
          "Content-Type": "application/json"
      },
      body: JSON.stringify(channel_url)
    })
      .then(res => res.json())
      .then(json => {
        console.log({json})
        console.log("channel data fetched", json)
        search_loading.value = false
        emit("search_completed", json)
      })
}

function search(channel_url) {
    console.log("searching")
    handleSearch(channel_url)
}

defineExpose({
    search
})

</script>

<template>
    <a-input-search
      v-model:value="search_keyword"
      placeholder="input search loading with enterButton"
      :loading="search_loading"
      size="large"
      @search="handleSearch"
      allowClear="true"
      enter-button
    />
</template>