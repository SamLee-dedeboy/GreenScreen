<script setup lang="ts">
import { Ref, VueElement, ref } from 'vue'
import * as vue from 'vue'

const emit = defineEmits(['search_completed'])
const search_keyword = ref('')
const search_loading = ref(false)


function handleSearch(keyword: string) {
    search_loading.value = true
    console.log(keyword)
    const result = {
        "some result": "blaablabla"
    }
    setTimeout(() => {
        search_loading.value = false
    }, 1000)
    emit("search_completed", result)
}

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